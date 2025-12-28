---
title: "Лицензии программного обеспечения I2P"
description: "Политика лицензирования и лицензии компонентов программного обеспечения, входящего в состав I2P"
slug: "licenses"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Как того требует наша [модель угроз](/docs/overview/threat-model//) (среди прочих причин), программное обеспечение, разработанное для поддержки сети анонимных коммуникаций, которую мы называем I2P, должно быть свободно доступным, с открытым исходным кодом и возможностью модификации пользователями. Чтобы соответствовать этим критериям, мы используем различные юридические и программные методы для устранения максимального количества барьеров на пути тех, кто рассматривает возможность использования I2P или внесения вклада в проект I2P.

Хотя информация ниже может показаться более запутанной, чем просто утверждение "I2P использует лицензию BSD", "I2P использует лицензию GPL" или "I2P находится в общественном достоянии", краткий ответ на вопрос "Какая лицензия у I2P?" следующий:

## Все программное обеспечение, входящее в состав дистрибутивов I2P, позволяет:

1. использование без платы
2. использование без ограничений на то, как, когда, где, почему или кем оно запускается
3. доступ к исходному коду без платы
4. модификации исходного кода

Большинство программного обеспечения гарантирует гораздо больше - возможность **любому** распространять модифицированный исходный код по своему усмотрению. Однако не все программное обеспечение в комплекте предоставляет такую свободу - GPL ограничивает возможности разработчиков, желающих интегрировать I2P со своими приложениями, которые сами не являются приложениями с открытым исходным кодом. Хотя мы приветствуем благородные цели увеличения ресурсов в общем достоянии, I2P лучше всего служит устранение любых барьеров, стоящих на пути его внедрения - если разработчик, рассматривающий возможность интеграции I2P со своим приложением, должен остановиться и проконсультироваться со своим юристом или провести аудит кода, чтобы убедиться, что их собственный исходный код может быть выпущен как совместимый с GPL, мы теряем возможности.

## Лицензии компонентов

Дистрибутив I2P содержит несколько ресурсов, отражающих разделение исходного кода на компоненты. Каждый компонент имеет свою собственную лицензию, с которой соглашаются все разработчики, вносящие в него вклад — либо путём явного объявления о выпуске кода под лицензией, совместимой с этим компонентом, либо путём неявного выпуска кода под основной лицензией компонента. У каждого из этих компонентов есть ведущий разработчик, который принимает окончательное решение о том, какая лицензия совместима с основной лицензией компонента, а менеджер проекта I2P принимает окончательное решение о том, какие лицензии соответствуют вышеуказанным четырём гарантиям для включения в дистрибутив I2P.

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

### Исключение GPL {#java_exception}

Хотя это может быть избыточным, для ясности код под GPL, включённый в I2PTunnel и другие приложения, должен распространяться под GPL с дополнительным «исключением», явно разрешающим использование стандартных библиотек Java:

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
Весь исходный код каждого компонента по умолчанию лицензируется в соответствии с основной лицензией, если в коде не указано иное. Всё вышеизложенное является кратким изложением условий лицензирования — пожалуйста, обратитесь к конкретной лицензии соответствующего компонента или исходного кода для получения точных условий. Местоположение исходных файлов компонентов и упаковка ресурсов могут быть изменены в случае реорганизации репозитория.

---

## Лицензия веб-сайта {#website}

Если не указано иное, содержимое этого сайта лицензировано под [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

---

## Доступ к коммитам {#commit}

Разработчики могут отправлять изменения в распределенный git-репозиторий, если получат разрешение от лица, управляющего этим репозиторием. Подробности смотрите в [Руководстве для новых разработчиков](/docs/develop/new-developers/).

Однако, чтобы изменения были включены в релиз, разработчики должны быть доверенными лицами у менеджера релизов (в настоящее время zzz). Кроме того, они должны явно согласиться с вышеуказанными условиями, чтобы получить доверие. Это означает, что они должны отправить одному из менеджеров релизов подписанное сообщение, подтверждающее, что:

- Если не указано иное, весь код, который я отправляю, неявно лицензируется в соответствии с основной лицензией компонента
- Если указано в исходном коде, код может быть явно лицензирован в соответствии с одной из альтернативных лицензий компонента
- Я имею право выпускать код, который я отправляю, на условиях, под которыми я его отправляю

Если кому-либо известны случаи, когда вышеуказанные условия не выполняются, пожалуйста, свяжитесь с руководителем компонента и/или менеджером релизов I2P для предоставления дополнительной информации.
