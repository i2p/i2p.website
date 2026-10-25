---
title: "软件更新规范"
description: "I2P 软件更新机制、SU3 文件格式和新闻订阅的规范说明"
slug: "updates"
aliases:
  - "/zh/updates"
  - "/zh/updates/"
category: "设计"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## 概述

I2P 使用一个简单而安全的系统来进行自动化软件更新。router 控制台会定期从一个可配置的 I2P URL 拉取新闻文件。还有一个硬编码的备用 URL 指向项目网站，以防默认的项目新闻主机出现故障。

新闻文件的内容显示在 router console 主页上。此外，新闻文件包含软件的最新版本号。如果版本号高于 router 的版本号，它将向用户显示有可用更新的提示。

如果配置为这样做，router 可以选择下载或下载并安装新版本。

## 旧新闻文件规范

此格式自 0.9.17 版本起已被 su3 新闻格式替代。

news.xml 文件可能包含以下元素：

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
i2p.release 条目中的参数如下。所有键都不区分大小写。所有值必须用双引号括起来。

**date** : router 版本的发布日期。未使用。格式未指定。

**minJavaVersion** : 运行当前版本所需的最低 Java 版本。自 0.9.9 版本起。

**minVersion** : 更新到当前版本所需的 router 最低版本。如果 router 版本低于此要求，用户必须先（手动？）更新到中间版本。自 0.9.9 版本开始。

**su3Clearnet** : 一个或多个可以在明网（非I2P网络）上找到.su3更新文件的HTTP URL。多个URL必须用空格或逗号分隔。自0.9.9版本起可用。

**su3SSL** : 一个或多个 HTTPS URLs，用于在明网（非 I2P 网络）上找到 .su3 更新文件。多个 URLs 必须用空格或逗号分隔。从 0.9.9 版本开始。

**sudTorrent** : 更新的 .sud（非 pack200）torrent 的磁力链接。自 0.9.4 版本起。

**su2Torrent**：更新的 .su2（pack200）torrent 的磁力链接。自 0.9.4 版本起。

**su3Torrent**：更新的 .su3（新格式）torrent 的磁力链接。自 0.9.9 版本起。

**version** : 必需。可用的最新当前 router 版本。

这些元素可以包含在 XML 注释中，以防止被浏览器解析。i2p.release 元素和版本是必需的。其他所有元素都是可选的。注意：由于解析器限制，整个元素必须在单行内。

## 更新文件规范

从 0.9.9 版本开始，名为 i2pupdate.su3 的签名更新文件将使用下面指定的 "su3" 文件格式。经批准的发布签名者将使用 4096 位 RSA 密钥。这些签名者的 X.509 公钥证书包含在 router 安装包中。更新可能包含新的、经批准的签名者的证书，和/或包含用于撤销的待删除证书列表。

## 旧更新文件规范

此格式自 0.9.9 版本起已过时。

签名的更新文件，传统上命名为 i2pupdate.sud，只是一个前面添加了 56 字节头部的 zip 文件。头部包含：

- 一个 40 字节的 DSA [Signature](/docs/specs/common-structures#signature)
- 一个 16 字节的 I2P 版本，采用 UTF-8 编码，如有必要用尾随零填充

签名仅覆盖zip存档 - 不包括前置的版本信息。签名必须匹配配置到router中的DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey)之一，router有一个硬编码的默认密钥列表，包含当前项目发布管理员的密钥。

出于版本比较的目的，版本字段包含 [0-9]*，字段分隔符为 '-'、'_' 和 '.'，所有其他字符都将被忽略。

从版本 0.8.8 开始，版本号还必须以 UTF-8 格式指定为 zip 文件注释，不包含尾随零。更新的 router 会验证头部中的版本号（不在签名覆盖范围内）是否与 zip 文件注释中的版本号匹配，而 zip 文件注释是在签名覆盖范围内的。这防止了头部中版本号的伪造。

## 下载与安装

router首先从可配置的I2P URL列表中的一个下载更新文件的头部，使用内置的HTTP客户端和代理，并检查版本是否更新。这防止了更新主机没有最新文件的问题。然后router下载完整的更新文件。router在安装前验证更新文件版本是否更新。当然，它也会验证签名，并验证zip文件注释是否与头部版本匹配，如上所述。

zip 文件被解压并复制到 I2P 配置目录中的 "i2pupdate.zip"（在 Linux 系统中为 ~/.i2p）。

从 0.7.12 版本开始，router 支持 Pack200 解压缩。zip 归档文件内带有 .jar.pack 或 .war.pack 后缀的文件会被透明地解压缩为 .jar 或 .war 文件。包含 .pack 文件的更新文件通常以 '.su2' 后缀命名。Pack200 可以将更新文件大小缩减约 60%。

从 0.8.7 版本开始，如果 zip 档案包含 lib/jbigi.jar 文件，router 将删除 libjbigi.so 和 libjcpuid.so 文件，以便从 jbigi.jar 中提取新文件。

从 0.8.12 版本开始，如果 zip 存档包含文件 deletelist.txt，router 将删除其中列出的文件。格式为：

- 每行一个文件名
- 所有文件名都相对于安装目录；不允许绝对文件名，不允许以".."开头的文件
- 注释以'#'开头

然后 router 会删除 deletelist.txt 文件。

## SU3 文件规范

此规范用于 0.9.9 版本以来的 router 更新、0.9.14 版本以来的重新种子数据、0.9.15 版本以来的插件，以及 0.9.17 版本以来的新闻文件。

### 之前的 .sud/.su2 格式存在的问题

- 没有魔数或标志
- 无法指定压缩、pack200或签名算法
- 版本不受签名保护，因此需要将其放在zip文件注释中（对于router文件）或plugin.config文件中（对于插件）来强制执行
- 未指定签名者，因此验证者必须尝试所有已知密钥
- 数据前签名格式需要两次传递来生成文件

### 目标

- 修复上述问题
- 迁移到更安全的签名算法
- 保持版本信息格式和偏移量不变，以兼容现有的版本检查器
- 一次性签名验证和文件提取

### 规范

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
所有未使用的字段必须设置为 0，以兼容未来版本。

### 签名详情

签名覆盖从字节 0 开始的整个头部，直到内容结束。我们使用原始签名。对数据进行哈希运算（使用字节 8-9 处签名类型所隐含的哈希类型），然后将其传递给"原始"签名或验证函数（例如 Java 中的 "NONEwithRSA"）。

虽然签名验证和内容提取可以在一次遍历中实现，但实现必须读取并缓冲前10个字节来确定哈希类型，然后才能开始验证。

各种签名类型的签名长度在[签名](/docs/specs/common-structures#signature)规范中给出。如有必要，用前导零填充签名。有关各种签名类型的参数，请参阅[密码学详细信息页面](/docs/specs/cryptography#sig)。

### 注意事项

内容类型指定信任域。对于每种内容类型，客户端维护一组 X.509 公钥证书，用于受信任签署该内容的各方。只能使用指定内容类型的证书。证书通过签名者的 ID 进行查找。客户端必须验证内容类型是否符合应用程序的预期。

所有值均采用网络字节序（大端序）。

要获得与 Java "NONEwithRSA" 兼容的原始 RSA 签名的 Python 实现，请参阅[这篇 Stack Overflow 文章](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)。

## SU3 Router 更新文件规范

### SU3 详细信息

- SU3 内容类型：1（ROUTER UPDATE）
- SU3 文件类型：0（ZIP）
- SU3 版本：router 版本

zip文件中的Jar和war文件不再使用pack200压缩（如上文"su2"文件所述），因为最新的Java运行时不再支持该功能。

### 注释

- 对于正式发布版本，SU3 版本是"基础" router 版本，例如 "0.9.20"。
- 对于开发构建版本，从 0.9.20 发布版本开始支持，SU3 版本是"完整" router 版本，例如 "0.9.20-5" 或 "0.9.20-5-rc"。请参阅 [I2P 源代码](https://github.com/i2p/i2p.i2p) 中的 RouterVersion.java。

## SU3 重新播种文件规范

从 0.9.14 版本开始，reseed 数据以 "su3" 文件格式提供。

### 目标

- 使用强签名和受信任证书对文件进行签名，以防止中间人攻击，避免受害者被引导到独立的不受信任网络中。
- 使用已在更新和插件中采用的 su3 文件格式
- 使用单个压缩文件加速重新播种过程，原本获取 200 个文件的过程十分缓慢

### 规范

1. 文件必须命名为 "i2pseeds.su3"。从 0.9.42 版本开始，请求方应该在请求 URL 后附加查询字符串 "?netid=2"，假设当前网络 ID 为 2。这可能用于防止跨网络连接。测试网络应该设置不同的网络 ID。详见提案 147。
2. 文件必须与 web 服务器上的 router info 文件位于同一目录中。
3. router 将首先尝试获取 (索引 URL)/i2pseeds.su3；如果失败，它将获取索引 URL，然后获取在链接中找到的各个 router info 文件。

### SU3 详细信息

- SU3 内容类型：3 (RESEED)
- SU3 文件类型：0 (ZIP)
- SU3 版本：自纪元以来的秒数，ASCII 格式 (date +%s)。不会在 2038 年或 2106 年发生翻转。
- zip 文件中的 router 信息文件必须位于"顶层"。zip 文件中没有目录。
- Router 信息文件必须命名为 "routerInfo-(44 字符 base 64 router 哈希).dat"，与旧的 reseed 机制相同。必须使用 I2P base 64 字母表。

### 注意事项

- 警告：已知多个 reseed 服务器通过 IPv6 无响应。建议强制或优先使用 IPv4。
- 警告：某些 reseed 服务器使用自签名 CA 证书。实现必须在 reseed 时导入并信任这些 CA，或者从 reseed 列表中省略自签名的 reseed 服务器。
- Reseed 签名者密钥以自签名 X.509 证书形式分发给实现，使用 RSA-4096 密钥（签名类型 6）。实现应强制执行证书中的有效日期。

## SU3 插件文件规范

从 0.9.15 版本开始，插件可以打包为 "su3" 文件格式。

### SU3 详细信息

- SU3 内容类型：2（插件）
- SU3 文件类型：0（ZIP）- 详情请参见[插件规范](/docs/specs/plugin)。
- SU3 版本：插件版本，必须与 plugin.config 中的版本匹配。

zip文件中的Jar和war文件不应该像上面"su2"文件文档中说明的那样使用pack200进行压缩，因为最新的Java运行时不再支持它。

## SU3 新闻文件规范

从 0.9.17 版本开始，新闻以 "su3" 文件格式传输。

### 目标

- 使用强签名和可信证书的签名新闻
- 使用已用于更新、重新播种和插件的 su3 文件格式
- 标准 XML 格式，可与标准解析器配合使用
- 标准 Atom 格式，可与标准订阅阅读器和生成器配合使用
- 在控制台显示前对 HTML 进行清理和验证
- 适合在 Android 和其他没有 HTML 控制台的平台上轻松实现

### SU3 详细信息

- SU3 Content Type: 4 (NEWS)
- SU3 File Type: 1 (XML) 或 3 (XML.GZ)
- SU3 Version: 自纪元以来的秒数，采用 ASCII 格式 (date +%s)。不会在 2038 年或 2106 年发生回滚。
- File Format: XML 或 gzipped XML，包含一个 [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom) XML Feed。字符集必须是 UTF-8。

### Atom Feed 详细信息

使用以下 `<feed>` 元素：

**`<entry>`** : 一条新闻项目。见下文。

**`<i2p:release>`** : I2P 更新元数据。见下文。

**`<i2p:revocations>`** : 证书撤销。见下文。

**`<i2p:blocklist>`** : 阻止列表数据。见下文。

**`<updated>`** : 必需的。feed的时间戳（符合 [RFC 4287](https://tools.ietf.org/html/rfc4287) 第3.3节和 [RFC 3339](https://tools.ietf.org/html/rfc3339)）。

### Atom 条目详情

新闻源中的每个 Atom `<entry>` 都可以在 router 控制台中被解析和显示。使用以下元素：

**`<author>`** : 可选。包含 `<name>` - 条目作者的姓名。

**`<content>`** : 必需。内容，必须是 type="xhtml"。XHTML 将通过允许元素的白名单和禁止属性的黑名单进行净化。当遇到非白名单元素时，客户端可以忽略该元素、或包含它的条目、或整个源。

**`<link>`** : 可选。用于获取更多信息的链接。

**`<summary>`** : 可选。简短摘要，适用于工具提示。

**`<title>`** : 必需。新闻条目的标题。

**`<updated>`** : 必需。此条目的时间戳（符合 [RFC 4287](https://tools.ietf.org/html/rfc4287) 第 3.3 节和 [RFC 3339](https://tools.ietf.org/html/rfc3339)）。

### Atom i2p:release 详情

源中必须至少包含一个 `<i2p:release>` 实体。每个实体包含以下属性和实体：

**date (属性)** : 必需。此条目的时间戳（符合 [RFC 4287](https://tools.ietf.org/html/rfc4287) 第3.3节和 [RFC 3339](https://tools.ietf.org/html/rfc3339)）。日期也可以使用截断格式 yyyy-mm-dd（不带 'T'）；这是 RFC 3339 中的"full-date"格式。在此格式下，任何处理过程都假定时间为 00:00:00 UTC。

**minJavaVersion (属性)** : 如果存在，表示运行当前版本所需的最低 Java 版本。

**minVersion (属性)** : 如果存在，表示更新到当前版本所需的 router 最低版本。如果 router 版本低于此版本，用户必须（手动？）先更新到中间版本。

**`<i2p:version>`** : 必需的。当前可用的最新 router 版本。

**`<i2p:update>`** : 更新文件（一个或多个）。它必须包含至少一个子元素。   - type（属性）："sud"、"su2" 或 "su3"。在所有 `<i2p:update>` 元素中必须唯一。   - `<i2p:clearnet>`：网络外直接下载链接（零个或多个）。href（属性）：标准的 clearnet http 链接。   - `<i2p:clearnetssl>`：网络外直接下载链接（零个或多个）。href（属性）：标准的 clearnet https 链接。   - `<i2p:torrent>`：网络内 magnet 链接。href（属性）：magnet 链接。   - `<i2p:url>`：网络内直接下载链接（零个或多个）。href（属性）：网络内 http .i2p 链接。

### Atom i2p:revocations 详情

这个实体是可选的，在 feed 中最多只能有一个 `<i2p:revocations>` 实体。此功能从 0.9.26 版本开始支持。

`<i2p:revocations>` 实体包含一个或多个 `<i2p:crl>` 实体。`<i2p:crl>` 实体包含以下属性：

**updated (属性)** : 必需。此条目的时间戳（符合 [RFC 4287](https://tools.ietf.org/html/rfc4287) 第 3.3 节和 [RFC 3339](https://tools.ietf.org/html/rfc3339)）。日期也可以采用截断格式 yyyy-mm-dd（不包含 'T'）；这是 RFC 3339 中的"完整日期"格式。在此格式中，进行任何处理时都假定时间为 00:00:00 UTC。

**id (属性)** : 必需。此 CRL 创建者的唯一标识符。

**(实体内容)** : 必需。一个标准的 base 64 编码证书吊销列表 (CRL)，包含换行符，以 '-----BEGIN X509 CRL-----' 行开始，以 '-----END X509 CRL-----' 行结束。有关 CRL 的更多信息，请参见 [RFC 5280](https://tools.ietf.org/html/rfc5280)。

### Atom i2p:blocklist 详情

此实体是可选的，feed 中最多只能有一个 `<i2p:blocklist>` 实体。此功能计划在 0.9.28 版本中实现。

`<i2p:blocklist>` 实体包含一个或多个 `<i2p:block>` 或 `<i2p:unblock>` 实体，一个 "updated" 实体，以及 "signer" 和 "sig" 属性：

**signer (属性)** : 必需。用于签署此阻止列表的公钥的唯一标识符 (UTF-8)。

**sig (属性)** : 必需。格式为 code:b64sig 的签名，其中 code 是 ASCII 签名类型编号，b64sig 是 base 64 编码的签名（I2P 字母表）。有关要签名的数据规范，请参见下文。

**`<updated>`** : 必需。阻止列表的时间戳（符合 [RFC 4287](https://tools.ietf.org/html/rfc4287) 第 3.3 节和 [RFC 3339](https://tools.ietf.org/html/rfc3339)）。日期也可以使用截断格式 yyyy-mm-dd（不包含 'T'）；这是 RFC 3339 中的 "full-date" 格式。在此格式中，处理时假定时间为 00:00:00 UTC。

**`<i2p:block>`** : 可选，允许多个实体。单个条目，可以是字面的 IPv4 或 IPv6 地址，或者是 44 字符的 base 64 router hash（I2P 字母表）。IPv6 地址可以使用缩写格式（包含 "::"）。对带有网络掩码的条目（例如 x.y.0.0/16）的支持是可选的。对主机名的支持是可选的。

**`<i2p:unblock>`** : 可选，允许多个实体。格式与 `<i2p:block>` 相同。

**签名规范：** 要生成待签名或验证的数据，请按以下顺序连接 ASCII 编码的数据：更新字符串后跟换行符（ASCII 0x0a），然后按接收顺序的每个阻止条目，每个条目后跟换行符，接着按接收顺序的每个解除阻止条目，每个条目后跟换行符。

## 阻止列表文件规范

待定，尚未实现，请参见提案 130。黑名单更新通过新闻文件传递，见上文。

## 未来工作

- router更新机制是网页router控制台的一部分。目前没有为缺少router控制台的嵌入式router提供更新功能。

## 参考文献

- **[CRYPTO-SIG]** [密码学 - 签名](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [I2P 源代码](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [插件规范](/docs/specs/plugin)
- **[Python]** [Python RSA 原始签名](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - 日期和时间](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Atom 聚合格式](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - 证书撤销列表](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [签名类型](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [SigningPublicKey 类型](/docs/specs/common-structures#signingpublickey)
