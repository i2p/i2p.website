---
title: "I2P 软件许可证"
description: "I2P 捆绑软件的许可证政策和组件许可证"
slug: "licenses"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

根据我们的[威胁模型](/docs/overview/threat-model//)（以及其他原因）的要求，为支持我们称之为I2P的匿名通信网络而开发的软件必须是免费可用、开源且用户可修改的。为了满足这些标准，我们采用了各种法律和软件工程技术，以尽可能消除那些考虑使用或为I2P项目做出贡献的人的进入障碍。

虽然下面的信息可能比简单地说"I2P是BSD"、"I2P是GPL"或"I2P是公共领域"更令人困惑,但对于"I2P如何授权?"这个问题的简短答案是：

## I2P 发行版中捆绑的所有软件将允许：

1. 免费使用
2. 使用时不受任何限制,包括使用方式、时间、地点、原因或使用者
3. 免费访问源代码
4. 修改源代码

大多数软件保证的更多——**任何人**都能以他们选择的方式分发修改后的源代码。然而，并非所有捆绑的软件都提供这种自由——GPL 限制了那些希望将 I2P 集成到自己非开源应用程序中的开发者的能力。虽然我们赞赏增加公共资源这一崇高目标，但最有利于 I2P 的做法是消除任何阻碍其采用的障碍——如果一个开发者在考虑是否可以将 I2P 集成到他们的应用程序时，不得不停下来咨询律师，或进行代码审计以确保他们自己的源代码可以作为 GPL 兼容版本发布，那我们就会失去机会。

## 组件许可证

I2P 发行版包含多个资源，反映了源代码被划分为多个组件。每个组件都有自己的许可证，所有为其做出贡献的开发者都同意该许可证——要么通过明确声明以与该组件兼容的许可证提交代码，要么通过隐式地以该组件的主要许可证提交代码。每个组件都有一位首席开发者，他对什么许可证与该组件的主要许可证兼容拥有最终决定权，而 I2P 项目经理对哪些许可证符合上述四项保证以纳入 I2P 发行版拥有最终决定权。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Source path</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Resource</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary license</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Alternate licenses</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Lead developer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P SDK</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">core</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P Router</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Ministreaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/ministreaming</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/bsd-license.php">BSD</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/streaming</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PTunnel</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/i2ptunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="#java_exception">GPL + exception</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a>, <a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Routerconsole</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/routerconsole</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.war</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Address Book</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/addressbook</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.war</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/bsd-license.php">BSD</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Susidns</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/susidns</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">susidns.war</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="#java_exception">GPL + exception</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Susimail</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/susimail</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">susimail.war</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="#java_exception">GPL + exception</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PSnark</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/i2psnark</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2psnark.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="#java_exception">GPL + exception</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong><a href="/docs/legacy/bob/">BOB</a> Bridge</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/BOB</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/WTFPL">WTFPL</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sponge</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong><a href="/docs/api/samv3/">SAM</a> Bridge</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/sam</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">zzz</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong><a href="/docs/legacy/sam/">SAM v1</a> Perl library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/sam/perl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM.pm</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://www.gnu.org/licenses/gpl-2.0.html">GPL</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BrianR</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong><a href="/docs/legacy/sam/">SAM v1</a> C library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/sam/c</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">libSAM</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/bsd-license.php">BSD</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Nightblade</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong><a href="/docs/legacy/sam/">SAM v1</a> Python library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/sam/python</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.py</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connelly</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong><a href="/docs/legacy/sam/">SAM v1</a> C# library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/sam/csharp/</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">smeghead</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Other apps not mentioned</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">apps/</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Probably <a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a> but check the source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Installer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">installer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">install.jar, guiinstall.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="https://en.wikipedia.org/wiki/Public_domain">Public domain</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><a href="#java_exception">GPL + exception</a>, <a href="http://opensource.org/licenses/bsd-license.php">BSD</a>, <a href="http://www.cryptix.org/LICENSE.TXT">Cryptix</a>, <a href="http://opensource.org/licenses/mit-license.html">MIT</a></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
    </tr>
  </tbody>
</table>

### GPL 例外 {#java_exception}

尽管这可能有些冗余,但为了明确起见,I2PTunnel 和其他应用程序中包含的 GPL 代码必须在 GPL 许可下发布,并附加一个"例外"条款,明确授权使用 Java 的标准库:

```
In addition, as a special exception, XXXX gives permission to link the
code of this program with the proprietary Java implementation provided by Sun
(or other vendors as well), and distribute linked combinations including the
two. You must obey the GNU General Public License in all respects for all of the
code used other than the proprietary Java implementation. If you modify this
file, you may extend this exception to your version of the file, but you are not
obligated to do so. If you do not wish to do so, delete this exception statement
from your version.
```
除非在代码中另有标注,否则每个组件下的所有源代码默认遵循主许可证。以上所有内容均为许可条款的摘要 - 请查阅相关组件或源代码的具体许可证以获取权威条款。如果仓库重新组织,组件源代码位置和资源打包方式可能会发生变化。

---

## 网站许可证 {#website}

除非另有说明,本站内容采用[知识共享署名-相同方式共享 4.0 国际许可协议](http://creativecommons.org/licenses/by-sa/4.0/)授权。

---

## 提交权限 {#commit}

如果您获得了运行该仓库的人员的许可,开发者可以将更改推送到分布式 git 仓库。详情请参阅[新开发者指南](/docs/develop/new-developers/)。

然而，要让更改被包含在发行版中，开发者必须得到发布管理员（目前是 zzz）的信任。此外，他们必须明确同意上述条款才能获得信任。这意味着他们必须向发布管理员之一发送一条签名消息，确认：

- 除非另有标明,我提交的所有代码都默认按照该组件的主要许可证进行授权
- 如果在源代码中指定,代码可能明确按照该组件的备用许可证之一进行授权
- 我有权按照我提交时的条款发布我提交的代码

如果有人发现任何不符合上述条件的情况，请联系组件负责人和/或 I2P 发布经理并提供进一步信息。
