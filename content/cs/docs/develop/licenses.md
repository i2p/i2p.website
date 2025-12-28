---
title: "Licence softwaru I2P"
description: "Licenční politika a licence komponent pro software dodávaný s I2P"
slug: "licenses"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Jak vyžaduje náš [model hrozeb](/docs/overview/threat-model//) (mimo jiné důvody), software vyvinutý pro podporu anonymní komunikační sítě, kterou nazýváme I2P, musí být volně dostupný, s otevřeným zdrojovým kódem a uživatelsky upravitelný. Abychom splnili tato kritéria, využíváme různé právní a softwarové inženýrské techniky, abychom odstranili co nejvíce překážek pro ty, kteří zvažují využití nebo přispění k projektu I2P.

Ačkoli níže uvedené informace mohou být matoucí spíše než jednoduché prohlášení "I2P je BSD", "I2P je GPL" nebo "I2P je veřejná doména", krátká odpověď na otázku "Jak je I2P licencováno?" zní takto:

## Veškerý software obsažený v distribucích I2P umožní:

1. použití bez poplatku
2. použití bez omezení jak, kdy, kde, proč nebo kým je provozováno
3. přístup ke zdrojovému kódu bez poplatku
4. úpravy zdrojového kódu

Většina softwaru zaručuje mnohem více - možnost **kohokoli** distribuovat upravený zdrojový kód jakýmkoli způsobem, který si zvolí. Ne všechen software, který je součástí balíčku, však poskytuje tuto svobodu - GPL omezuje možnosti vývojářů, kteří si přejí integrovat I2P se svými vlastními aplikacemi, které samy nejsou aplikacemi s otevřeným zdrojovým kódem. Zatímco oceňujeme ušlechtilé cíle zvyšování zdrojů ve veřejném prostoru, I2P je nejlépe slouženo odstraněním jakýchkoli překážek, které stojí v cestě jeho přijetí - pokud vývojář zvažující, zda může integrovat I2P se svou aplikací, musí zastavit a poradit se se svým právníkem nebo provést audit kódu, aby se ujistil, že jejich vlastní zdrojový kód může být zveřejněn jako kompatibilní s GPL, přicházíme zkrátka.

## Licence komponent

Distribuce I2P obsahuje několik zdrojů, které odrážejí rozdělení zdrojového kódu do komponent. Každá komponenta má svou vlastní licenci, se kterou všichni vývojáři, kteří k ní přispívají, souhlasí - buď explicitním prohlášením o vydání kódu zapsaného pod licencí kompatibilní s danou komponentou, nebo implicitním vydáním kódu zapsaného pod primární licencí komponenty. Každá z těchto komponent má vedoucího vývojáře, který má konečné slovo ohledně toho, která licence je kompatibilní s primární licencí komponenty, a projektový manažer I2P má konečné slovo ohledně toho, které licence splňují výše uvedené čtyři záruky pro zařazení do distribuce I2P.

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

### Výjimka GPL {#java_exception}

Ačkoli to může být nadbytečné, jen pro jistotu musí být kód pod licencí GPL zahrnutý v I2PTunnel a dalších aplikacích vydán pod GPL s dodatečnou "výjimkou", která explicitně povoluje použití standardních knihoven Javy:

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
Veškerý zdrojový kód každé komponenty bude ve výchozím nastavení licencován pod primární licencí, pokud není v kódu označeno jinak. Vše výše uvedené je shrnutím licenčních podmínek – pro závazné podmínky se prosím podívejte na konkrétní licenci dané komponenty nebo zdrojového kódu. Umístění zdrojových kódů komponent a balení zdrojů může být změněno v případě reorganizace repozitáře.

---

## Licence webu {#website}

Pokud není uvedeno jinak, obsah těchto stránek je licencován pod [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

---

## Přístup k commitům {#commit}

Vývojáři mohou odesílat změny do distribuovaného git repozitáře, pokud získají oprávnění od osoby spravující daný repozitář. Podrobnosti naleznete v [Průvodci pro nové vývojáře](/docs/develop/new-developers/).

Aby však byly změny zahrnuty do vydání, musí vývojáři získat důvěru správce vydání (v současnosti zzz). Kromě toho musí výslovně souhlasit s výše uvedenými podmínkami, aby získali důvěru. To znamená, že musí poslat jednomu ze správců vydání podepsanou zprávu potvrzující, že:

- Pokud není označeno jinak, veškerý kód, který commituji, je implicitně licencován pod primární licencí komponenty
- Pokud je to uvedeno ve zdrojovém kódu, kód může být explicitně licencován pod jednou z alternativních licencí komponenty
- Mám právo uvolnit kód, který commituji, za podmínek, pod kterými jej commituji

Pokud je vám známa jakákoli situace, kdy výše uvedené podmínky nejsou splněny, kontaktujte prosím vedoucího komponenty a/nebo správce vydání I2P s dalšími informacemi.
