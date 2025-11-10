---
title: "I2P ist von der log4j-Sicherheitslücke nicht betroffen."
date: 2021-12-11
author: "idk, zzz"
description: "I2P verwendet kein log4j und ist daher von CVE-2021-44228 nicht betroffen"
categories: ["security"]
API_Translate: wahr
---

I2P ist von der log4j-0-Day-Sicherheitslücke, die gestern veröffentlicht wurde, CVE-2021-44228, nicht betroffen. I2P verwendet log4j nicht für das Logging; dennoch mussten wir unsere Abhängigkeiten auf die Verwendung von log4j überprüfen, insbesondere jetty. Diese Überprüfung hat keine Schwachstellen ergeben.

Es war auch wichtig, all unsere Plugins zu überprüfen. Plugins können ihre eigenen Logging-Systeme mitbringen, einschließlich log4j. Wir stellten fest, dass die meisten Plugins ebenfalls kein log4j verwenden und diejenigen, die es tun, keine verwundbare Version von log4j verwendeten.

Wir haben keine Abhängigkeiten, Plugins oder Apps gefunden, die verwundbar sind.

We bundle a log4j.properties file with jetty for plugins that introduce log4j. This file only has an effect on plugins which use log4j logging internally. We have checked in the recommended mitigation to the log4j.properties file. Plugins which enable log4j will run with the vulnerable feature disabled. As we cannot find any usage of log4j 2.x anywhere, we have no plans to do an emergency release at this time.
