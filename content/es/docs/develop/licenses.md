---
title: "Licencias de Software de I2P"
description: "Política de licencias y licencias de componentes para el software incluido con I2P"
slug: "licenses"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Como requiere nuestro [modelo de amenazas](/docs/overview/threat-model//) (entre otras razones), el software desarrollado para soportar la red de comunicación anónima que llamamos I2P debe estar disponible libremente, ser de código abierto y modificable por el usuario. Para cumplir con estos criterios, hacemos uso de una variedad de técnicas legales y de ingeniería de software con el fin de eliminar tantas barreras de entrada como sea posible para aquellos que consideren hacer uso de I2P o contribuir al proyecto.

Aunque la información a continuación puede ser más confusa que simplemente decir "I2P es BSD", "I2P es GPL" o "I2P es de dominio público", la respuesta corta a la pregunta "¿Cómo está licenciado I2P?" es esta:

## Todo el software incluido en las distribuciones de I2P permitirá:

1. uso sin cargo
2. uso sin restricciones sobre cómo, cuándo, dónde, por qué o quién lo ejecuta
3. acceso al código fuente sin cargo
4. modificaciones al código fuente

La mayoría del software garantiza mucho más: la capacidad de **cualquiera** para distribuir el código fuente modificado como desee. Sin embargo, no todo el software incluido proporciona esta libertad - la GPL restringe la capacidad de los desarrolladores que desean integrar I2P con sus propias aplicaciones que no son en sí mismas aplicaciones de código abierto. Si bien aplaudimos los nobles objetivos de aumentar los recursos en los bienes comunes, I2P se beneficia mejor eliminando cualquier barrera que obstaculice su adopción - si un desarrollador que está considerando si puede integrar I2P con su aplicación tiene que detenerse y consultar con su abogado, o realizar una auditoría de código para asegurarse de que su propio código fuente pueda publicarse como compatible con GPL, perdemos oportunidades.

## Licencias de componentes

La distribución de I2P contiene varios recursos, reflejando la partición del código fuente en componentes. Cada componente tiene su propia licencia, con la cual todos los desarrolladores que contribuyen a él están de acuerdo - ya sea declarando explícitamente la liberación del código comprometido bajo una licencia compatible con ese componente, o liberando implícitamente el código comprometido bajo la licencia principal del componente. Cada uno de estos componentes tiene un desarrollador líder que tiene la última palabra en cuanto a qué licencia es compatible con la licencia principal del componente, y el gestor del proyecto I2P tiene la última palabra en cuanto a qué licencias cumplen las cuatro garantías mencionadas anteriormente para su inclusión en la distribución de I2P.

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

### Excepción GPL {#java_exception}

Si bien puede ser redundante, solo para mayor claridad, el código con licencia GPL incluido en I2PTunnel y otras aplicaciones debe publicarse bajo la GPL con una "excepción" adicional que autorice explícitamente el uso de las bibliotecas estándar de Java:

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
Todo el código fuente bajo cada componente estará licenciado por defecto bajo la licencia principal, a menos que se indique lo contrario en el código. Todo lo anterior es un resumen de los términos de la licencia - por favor consulte la licencia específica del componente o código fuente en cuestión para los términos oficiales. Las ubicaciones de origen de los componentes y el empaquetado de recursos pueden cambiar si el repositorio se reorganiza.

---

## Licencia del Sitio Web {#website}

Excepto donde se indique lo contrario, el contenido de este sitio está licenciado bajo una [Licencia Creative Commons Atribución-CompartirIgual 4.0 Internacional](http://creativecommons.org/licenses/by-sa/4.0/).

---

## Acceso de Commit {#commit}

Los desarrolladores pueden enviar cambios a un repositorio git distribuido si reciben permiso de la persona que administra ese repositorio. Consulta la [Guía para Nuevos Desarrolladores](/docs/develop/new-developers/) para más detalles.

Sin embargo, para que los cambios se incluyan en una versión, los desarrolladores deben ser confiables para el gestor de lanzamientos (actualmente zzz). Además, deben estar explícitamente de acuerdo con los términos anteriores para ser confiables. Esto significa que deben enviar a uno de los gestores de lanzamientos un mensaje firmado afirmando que:

- A menos que se indique lo contrario, todo el código que envío está implícitamente licenciado bajo la licencia principal del componente
- Si se especifica en el código fuente, el código puede estar explícitamente licenciado bajo una de las licencias alternativas del componente
- Tengo el derecho de publicar el código que envío bajo los términos con los que lo estoy enviando

Si alguien tiene conocimiento de algún caso en el que no se cumplan las condiciones anteriores, por favor contacte al responsable del componente y/o a un administrador de lanzamientos de I2P con más información.
