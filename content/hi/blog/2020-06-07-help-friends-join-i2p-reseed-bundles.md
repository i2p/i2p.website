---
title: "Reseed Bundles साझा करके अपने मित्रों को I2P से जुड़ने में मदद करें"
date: 2020-06-07
author: "idk"
description: "reseed bundles बनाएँ, आदान-प्रदान करें, और उपयोग करें"
categories: ["reseed"]
---

अधिकांश नए I2P routers किसी reseed service की मदद से बूटस्ट्रैपिंग करके नेटवर्क से जुड़ते हैं। हालांकि, reseed services केंद्रीकृत होती हैं और तुलनात्मक रूप से आसानी से ब्लॉक की जा सकती हैं, जबकि I2P नेटवर्क के बाकी हिस्से में विकेंद्रीकृत और ब्लॉक न किए जा सकने वाले कनेक्शनों पर जोर दिया जाता है। यदि कोई नया I2P router बूटस्ट्रैप करने में असमर्थ हो, तो किसी मौजूदा I2P router का उपयोग करके एक कार्यशील "Reseed bundle" तैयार करना और reseed service की आवश्यकता के बिना बूटस्ट्रैप करना संभव हो सकता है।

एक कार्यरत I2P कनेक्शन वाला उपयोगकर्ता, एक अवरुद्ध router को नेटवर्क से जुड़ने में मदद कर सकता है, एक reseed (प्रारंभिक नेटवर्क जानकारी) फ़ाइल बनाकर और उसे गोपनीय या अप्रतिबंधित चैनल के माध्यम से भेजकर। वास्तव में, कई परिस्थितियों में, पहले से जुड़ा हुआ I2P router reseed ब्लॉकिंग से बिल्कुल प्रभावित नहीं होगा, इसलिए **आसपास कार्यरत I2P routers होने का मतलब है कि मौजूदा I2P routers, नए I2P routers को बूटस्ट्रैपिंग का एक छिपा तरीका प्रदान करके मदद कर सकते हैं**.

## Reseed बंडल तैयार करना

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## फ़ाइल से Reseed करना

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
