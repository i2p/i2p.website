---
title: "Easy-Install für Windows 2.3.0 veröffentlicht"
date: 2023-07-10
author: "idk"
description: "Easy-Install für Windows 2.3.0 veröffentlicht"
categories: ["release"]
API_Translate: wahr
---

Das I2P Easy-Install-Bundle für Windows in der Version 2.3.0 wurde jetzt freigegeben. Wie üblich enthält diese Veröffentlichung eine aktualisierte Version des I2P router. Dies umfasst auch Sicherheitsprobleme, die Personen betreffen, die Dienste im Netzwerk betreiben.

Dies wird das letzte Release des Easy-Install bundle sein, das mit der I2P Desktop GUI inkompatibel ist. Es wurde aktualisiert und enthält nun neue Versionen aller mitgelieferten WebExtensions. Ein langjähriger Fehler in I2P in Private Browsing, der es mit benutzerdefinierten Themes inkompatibel machte, wurde behoben. Nutzern wird weiterhin geraten, *keine* benutzerdefinierten Themes zu installieren. Snark-Tabs werden in Firefox nicht automatisch an den Anfang der Tab-Reihenfolge angeheftet. Abgesehen von der Verwendung alternativer cookieStores verhalten sich Snark-Tabs jetzt wie normale Browser-Tabs.

**Leider ist diese Version weiterhin ein unsigniertes `.exe`-Installationsprogramm.** Bitte überprüfen Sie die Prüfsumme des Installationsprogramms, bevor Sie es verwenden. **Die Updates hingegen** sind mit meinen I2P-Signaturschlüsseln signiert und daher sicher.

Diese Version wurde mit OpenJDK 20 kompiliert. Sie verwendet i2p.plugins.firefox Version 1.1.0 als Bibliothek zum Starten des Browsers. Sie verwendet i2p.i2p Version 2.3.0 als I2P router und zur Bereitstellung von Anwendungen. Wie immer wird empfohlen, den I2P router so bald wie es Ihnen möglich ist auf die neueste Version zu aktualisieren.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
