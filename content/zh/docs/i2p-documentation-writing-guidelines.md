---
title: "I2P 文档撰写指南"
description: "在整个 I2P 技术文档中保持一致性、准确性和可访问性"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**目的:** 确保 I2P 技术文档的一致性、准确性和可访问性

---

## 核心原则

### 1. 验证一切

**切勿臆测或猜测。** 所有技术陈述都必须依据以下内容进行核验： - 当前的 I2P 源代码 (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - 官方 API 文档 (https://i2p.github.io/i2p.i2p/  - 配置规范 [/docs/specs/](/docs/) - 最新发行说明 [/releases/](/categories/release/)

**正确验证的示例：**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. 清晰优先于简洁

写给可能第一次接触 I2P 的开发者。不要假定读者已有相关知识，应当完整、充分地解释各个概念。

**示例：**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. 无障碍优先

尽管 I2P 是一个叠加网络，文档仍必须在明网（常规互联网）上对开发者可用。请始终为 I2P 内部资源提供可在明网访问的替代方案。

---

## 技术准确性

### API 与接口文档

**务必包含：** 1. 首次出现时使用完整的包名：`net.i2p.app.ClientApp` 2. 包含返回类型的完整方法签名 3. 参数名称和类型 4. 必需参数与可选参数

**示例：**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### 配置属性

在编写配置文件文档时：
1. 显示精确的属性名称
2. 指定文件编码（I2P 配置文件使用 UTF-8）
3. 提供完整的示例
4. 记录默认值
5. 注明属性引入/更改的版本

**示例：**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### 常量和枚举

在为常量编写文档时，请使用代码中的真实名称：

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### 区分相似概念

I2P 包含多个相互重叠的系统。撰写文档时务必明确你所描述的是哪个系统：

**示例：**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## 文档链接与参考资料

### URL 可访问性规则

1. **主要参考** 应使用可从明网访问的 URL
2. **I2P 内部 URL** (.i2p 域名) 必须包含可访问性说明
3. **始终提供替代方案**，在链接 I2P 内部资源时

**I2P 内部 URL 模板:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### 推荐的 I2P 参考链接

**官方规范：** - [配置](/docs/specs/configuration/) - [插件](/docs/specs/plugin/) - [文档索引](/docs/)

**API 文档（选择最新的）：** - 最新: https://i2p.github.io/i2p.i2p/ (在 I2P 2.10.0 中为 API 0.9.66) - 明网镜像: https://eyedeekay.github.io/javadoc-i2p/

**源代码:** - GitLab (官方): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - GitHub 镜像: https://github.com/i2p/i2p.i2p

### 链接格式标准

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## 版本跟踪

### 文档元数据

每份技术文档都应在 frontmatter（文档头部）中包含版本元数据：

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**字段定义:** - `lastUpdated`: 文档上次审阅/更新的年月 - `accurateFor`: 该文档已核对所对应的 I2P 版本 - `reviewStatus`: 取值之一："draft"、"needs-review"、"verified"、"outdated"

### 内容中的版本引用

在提及版本时: 1. 对当前版本使用**加粗**: "**版本 2.10.0** (2025年9月)" 2. 历史参考中应同时注明版本号和日期 3. 在相关情况下，将 API 版本与 I2P 版本分开注明

**示例：**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### 记录随时间推移的变更

对于已经演进的特性：

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### 弃用通知

如果为已弃用功能编写文档：

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## 术语标准

### I2P 官方术语

请始终一致地使用这些确切术语：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### 托管客户端术语

在为受管客户端撰写文档时：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### 配置术语

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### 包和类名

首次提及时始终使用全称，此后使用简称：

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## 代码示例与格式

### Java 代码示例

使用正确的语法高亮和完整的示例：

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**代码示例要求：** 1. 包含注释以解释关键代码行 2. 在相关处展示错误处理 3. 使用贴近实际的变量名 4. 符合 I2P 编码约定 (4 空格缩进) 5. 若上下文不明显，请展示导入语句

### 配置示例

展示完整、有效的配置示例：

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### 命令行示例

用户命令使用 `$`，root 使用 `#`：

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### 行内代码

对以下内容使用反引号： - 方法名: `startup()` - 类名: `ClientApp` - 属性名: `clientApp.0.main` - 文件名: `clients.config` - 常量: `SVC_HTTP_PROXY` - 包名: `net.i2p.app`

---

## 语气与文风

### 专业而易懂

面向技术受众撰写，避免居高临下：

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### 主动语态

为清晰起见，请使用主动语态：

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### 用于指令的祈使句

在步骤性内容中使用直接祈使语气：

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### 避免不必要的术语

首次出现时解释术语：

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### 标点符号指南

1. **不要使用长破折号** - 请改用短横线、逗号或分号
2. 在列表中使用**牛津逗号**: "console, i2ptunnel, and Jetty"
3. **代码块内的句号** 仅在语法确有必要时使用
4. **并列列表** 当列表项包含逗号时使用分号

---

## 文档结构

### 标准章节顺序

有关 API 文档：

1. **概述** - 该功能的作用及其存在的原因
2. **实现** - 如何实现/使用它
3. **配置** - 如何进行配置
4. **API 参考** - 方法/属性的详细说明
5. **示例** - 完整可运行示例
6. **最佳实践** - 提示与建议
7. **版本历史** - 引入时间及其随时间的变更
8. **参考资料** - 相关文档的链接

### 标题层次结构

使用语义化的标题层级：

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### 信息框

对于特殊通知，请使用块引用：

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### 列表与组织

**无序列表** 用于非顺序项：

```markdown
- First item
- Second item
- Third item
```
**有序列表** 用于顺序步骤：

```markdown
1. First step
2. Second step
3. Third step
```
**定义列表** 用于术语解释:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## 应避免的常见陷阱

### 1. 容易混淆的相似系统

**不要混淆：** - ClientAppManager（客户端应用管理器）注册表 与 PortMapper（端口映射器） - i2ptunnel 的 tunnel（隧道）类型 与 端口映射器服务常量 - ClientApp（客户端应用） 与 RouterApp（Router 应用）（上下文不同） - 受管 与 非受管 客户端

**务必明确是哪一个系统** 你正在讨论：

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. 过时的版本引用

**不要：** - 将旧版本称为“当前” - 链接到过时的 API 文档 - 在示例中使用已弃用的方法签名

**应做：** - 在发布前检查发行说明 - 验证 API 文档与当前版本一致 - 更新示例以使用当前最佳实践

### 3. 无法访问的 URL

**不要:** - 仅链接到 .i2p 域名且没有 clearnet（公开互联网）替代方案 - 使用失效或过时的文档 URL - 链接到本地的 file:// 路径

**应当：** - 为所有 I2P 内部链接提供明网替代链接 - 在发布前确认 URL 可访问 - 使用长期可用的 URL（geti2p.net，而非临时托管）

### 4. 不完整的代码示例

**不要：** - 在没有上下文的情况下展示代码片段 - 省略错误处理 - 使用未定义的变量 - 在不明显的情况下省略 import 语句

**应当：** - 展示完整、可编译的示例 - 包含必要的错误处理 - 解释每一行关键代码的作用 - 在发布前对示例进行测试

### 5. 含糊不清的表述

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Markdown 约定

### 文件命名

对文件名使用 kebab-case（短横线命名法）： - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### 前置元数据格式

始终包含 YAML 头部信息：

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### 链接格式

**内部链接** (文档内):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**外部链接**（指向其他资源）：

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**代码仓库链接**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### 表格格式设置

使用 GitHub 风格的 Markdown 表格：

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### 代码块语言标签

始终为语法高亮指定语言：

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## 评审清单

在发布文档之前，请确认：

- [ ] 所有技术论断均已通过源代码或官方文档验证
- [ ] 版本号和日期为最新
- [ ] 所有 URL 可从明网访问（或已提供替代方案）
- [ ] 代码示例完整并经过测试
- [ ] 术语遵循 I2P 约定
- [ ] 不使用 em-dash（长破折号），使用普通短横线或其他标点
- [ ] Frontmatter（前置元数据）完整且准确
- [ ] 标题层级语义化（h1 → h2 → h3）
- [ ] 列表和表格格式正确
- [ ] 参考部分包含所有被引用的来源
- [ ] 文档遵循结构指南
- [ ] 语气专业但易于理解
- [ ] 相近概念有清晰区分
- [ ] 无失效链接或引用
- [ ] 配置示例有效且为最新

---

**反馈：** 如果你发现问题或对这些指南有任何建议，请通过 I2P 官方开发渠道提交。
