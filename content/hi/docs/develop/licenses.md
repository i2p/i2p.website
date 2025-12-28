---
title: "I2P सॉफ़्टवेयर लाइसेंस"
description: "I2P के साथ बंडल किए गए सॉफ़्टवेयर के लिए लाइसेंस नीति और घटक लाइसेंस"
slug: "licenses"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

जैसा कि हमारे [threat model](/docs/overview/threat-model//) (अन्य कारणों के साथ) द्वारा आवश्यक है, I2P नामक anonymous communication network को समर्थन देने के लिए विकसित सॉफ्टवेयर स्वतंत्र रूप से उपलब्ध, open source, और उपयोगकर्ता द्वारा संशोधनीय होना चाहिए। इन मानदंडों को पूरा करने के लिए, हम विभिन्न कानूनी और software engineering तकनीकों का उपयोग करते हैं ताकि I2P के उपयोग या योगदान पर विचार करने वालों के लिए प्रवेश में आने वाली बाधाओं को यथासंभव कम किया जा सके।

जबकि नीचे दी गई जानकारी केवल "I2P, BSD है", "I2P, GPL है", या "I2P सार्वजनिक डोमेन है" कहने की तुलना में अधिक भ्रमित करने वाली हो सकती है, "I2P को कैसे लाइसेंस दिया गया है?" इस प्रश्न का संक्षिप्त उत्तर यह है:

## I2P वितरण में बंडल किए गए सभी सॉफ़्टवेयर निम्नलिखित की अनुमति देंगे:

1. बिना शुल्क के उपयोग
2. कैसे, कब, कहाँ, क्यों, या किसके द्वारा चलाया जा रहा है, इस पर बिना किसी प्रतिबंध के उपयोग
3. बिना शुल्क के source code तक पहुँच
4. source में संशोधन

अधिकांश सॉफ्टवेयर इससे कहीं अधिक की गारंटी देते हैं - **किसी भी व्यक्ति** की संशोधित स्रोत कोड को अपनी इच्छानुसार वितरित करने की क्षमता। हालांकि, बंडल किए गए सभी सॉफ्टवेयर यह स्वतंत्रता प्रदान नहीं करते - GPL उन डेवलपर्स की क्षमता को प्रतिबंधित करता है जो I2P को अपने स्वयं के अनुप्रयोगों के साथ एकीकृत करना चाहते हैं जो स्वयं open source अनुप्रयोग नहीं हैं। जबकि हम सामान्य संसाधनों को बढ़ाने के महान लक्ष्यों की सराहना करते हैं, I2P की सबसे अच्छी सेवा इसकी स्वीकृति के रास्ते में आने वाली किसी भी बाधा को हटाने से होती है - यदि कोई डेवलपर यह विचार कर रहा है कि क्या वे I2P को अपने अनुप्रयोग के साथ एकीकृत कर सकते हैं, और उन्हें रुककर अपने वकील से जांच करनी पड़े, या यह सुनिश्चित करने के लिए कोड ऑडिट करना पड़े कि उनका अपना स्रोत कोड GPL-संगत के रूप में जारी किया जा सकता है, तो हम इसे खो देते हैं।

## घटक लाइसेंस

I2P वितरण में कई संसाधन शामिल हैं, जो स्रोत कोड को घटकों में विभाजन को दर्शाते हैं। प्रत्येक घटक का अपना लाइसेंस होता है, जिससे उसमें योगदान करने वाले सभी डेवलपर्स सहमत होते हैं - या तो उस घटक के साथ संगत लाइसेंस के तहत प्रतिबद्ध कोड की रिलीज़ को स्पष्ट रूप से घोषित करके, या घटक के प्राथमिक लाइसेंस के तहत प्रतिबद्ध कोड को अप्रत्यक्ष रूप से जारी करके। इन घटकों में से प्रत्येक का एक प्रमुख डेवलपर होता है जिसका अंतिम निर्णय होता है कि कौन सा लाइसेंस घटक के प्राथमिक लाइसेंस के साथ संगत है, और I2P परियोजना प्रबंधक का अंतिम निर्णय होता है कि कौन से लाइसेंस I2P वितरण में शामिल करने के लिए उपरोक्त चार गारंटियों को पूरा करते हैं।

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

### GPL अपवाद {#java_exception}

हालांकि यह अनावश्यक हो सकता है, लेकिन स्पष्टता के लिए I2PTunnel और अन्य ऐप्स में शामिल GPL'ed कोड को GPL के तहत जारी किया जाना चाहिए, जिसमें Java की मानक लाइब्रेरी के उपयोग को स्पष्ट रूप से अधिकृत करने वाला एक अतिरिक्त "अपवाद" होना चाहिए:

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
प्रत्येक घटक के अंतर्गत सभी स्रोत कोड डिफ़ॉल्ट रूप से प्राथमिक लाइसेंस के तहत लाइसेंस प्राप्त होगा, जब तक कि कोड में अन्यथा चिह्नित न किया गया हो। उपरोक्त सभी लाइसेंस शर्तों का सारांश है - कृपया आधिकारिक शर्तों के लिए संबंधित घटक या स्रोत कोड का विशिष्ट लाइसेंस देखें। यदि रिपॉजिटरी को पुनर्गठित किया जाता है तो घटक स्रोत स्थान और संसाधन पैकेजिंग को बदला जा सकता है।

---

## वेबसाइट लाइसेंस {#website}

जहाँ अन्यथा उल्लेख न किया गया हो, इस साइट पर सामग्री [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/) के तहत लाइसेंस प्राप्त है।

---

## कमिट एक्सेस {#commit}

डेवलपर्स वितरित git रिपॉजिटरी में परिवर्तन push कर सकते हैं यदि आपको उस रिपॉजिटरी को चलाने वाले व्यक्ति से अनुमति मिलती है। विवरण के लिए [New Developer Guide](/docs/develop/new-developers/) देखें।

हालांकि, किसी रिलीज़ में बदलावों को शामिल करने के लिए, डेवलपर्स को रिलीज़ मैनेजर (वर्तमान में zzz) द्वारा विश्वसनीय होना चाहिए। इसके अलावा, उन्हें विश्वसनीय होने के लिए उपरोक्त शर्तों से स्पष्ट रूप से सहमत होना चाहिए। इसका मतलब है कि उन्हें रिलीज़ मैनेजर्स में से किसी एक को एक हस्ताक्षरित संदेश भेजना होगा जिसमें यह पुष्टि हो कि:

- जब तक अन्यथा चिह्नित न हो, मेरे द्वारा commit किया गया सभी कोड स्वतः घटक के प्राथमिक लाइसेंस के तहत लाइसेंस प्राप्त है
- यदि स्रोत में निर्दिष्ट है, तो कोड स्पष्ट रूप से घटक के वैकल्पिक लाइसेंसों में से किसी एक के तहत लाइसेंस प्राप्त हो सकता है
- मुझे अपने द्वारा commit किए गए कोड को उन शर्तों के तहत जारी करने का अधिकार है जिनके तहत मैं इसे commit कर रहा हूं

यदि किसी को ऐसी कोई स्थिति के बारे में जानकारी है जहाँ उपरोक्त शर्तें पूरी नहीं होती हैं, तो कृपया अधिक जानकारी के साथ component lead और/या I2P release manager से संपर्क करें।
