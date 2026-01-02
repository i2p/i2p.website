---
title: "I2P के साथ IDE का उपयोग"
description: "Eclipse और NetBeans को Gradle और बंडल किए गए प्रोजेक्ट फाइलों के साथ I2P विकास के लिए सेटअप करें"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: दस्तावेज़
reviewStatus: "needs-review"
---

<p> मुख्य I2P विकास ब्रांच (<code>i2p.i2p</code>) को डेवलपर्स के लिए Java विकास के दो सामान्य रूप से उपयोग किए जाने वाले IDEs को आसानी से सेट अप करने में सक्षम बनाने के लिए स्थापित किया गया है: Eclipse और NetBeans। </p>

<h2>Eclipse</h2>

<p> मुख्य I2P विकास शाखाएँ (<code>i2p.i2p</code> और इससे निकली शाखाएँ) में <code>build.gradle</code> शामिल है ताकि शाखा को Eclipse में आसानी से सेटअप किया जा सके। </p>

<ol> <li> सुनिश्चित करें कि आपके पास Eclipse का हाल का संस्करण है। 2017 से नया कोई भी संस्करण काम करेगा। </li> <li> I2P branch को किसी डायरेक्टरी में check out करें (जैसे <code>$HOME/dev/i2p.i2p</code>)। </li> <li> "File → Import..." चुनें और फिर "Gradle" के अंतर्गत "Existing Gradle Project" चुनें। </li> <li> "Project root directory:" के लिए वह डायरेक्टरी चुनें जिसमें I2P branch को check out किया गया था। </li> <li> "Import Options" डायलॉग में, "Gradle Wrapper" चुनें और Continue दबाएं। </li> <li> "Import Preview" डायलॉग में आप प्रोजेक्ट संरचना की समीक्षा कर सकते हैं। "i2p.i2p" के अंतर्गत कई प्रोजेक्ट दिखाई देने चाहिए। "Finish" दबाएं। </li> <li> हो गया! आपके workspace में अब I2P branch के भीतर सभी प्रोजेक्ट होने चाहिए, और उनकी build dependencies सही तरीके से सेट होनी चाहिए। </li> </ol>

<h2>NetBeans</h2>

<p> मुख्य I2P विकास ब्रांचेस (<code>i2p.i2p</code> और इससे बनी ब्रांचेस) में NetBeans प्रोजेक्ट फाइलें शामिल हैं। </p>

<!-- सामग्री को न्यूनतम और मूल के करीब रखें; बाद में अपडेट करेंगे। -->
