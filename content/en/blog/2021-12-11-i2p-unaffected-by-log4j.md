---
title: "I2P is not affected by the log4j vulnerability"
date: 2021-12-11
author: "idk, zzz"
description: "I2P doesn't use log4j and is therefore unaffected by CVE-2021-44228"
categories: ["security"]
---

I2P is not affected by the log4j 0-Day vulnerability which was published yesterday, CVE-2021-44228. I2P doesn't use log4j for logging, however we also needed to review our dependencies for log4j usage, especially jetty. This review has not revealed any vulnerabilities.

It was also important to check all of our plugins. Plugins may bring in their own logging systems, including log4j. We found that most plugins also do not use log4j, and those that do did not use a vulnerable version of log4j.

We haven't found any dependency, plugin or app that's vulnerable.

We bundle a log4j.properties file with jetty for plugins that introduce log4j. This file only has an effect on plugins which use log4j logging internally. We have checked in the recommended mitigation to the log4j.properties file. Plugins which enable log4j will run with the vulnerable feature disabled. As we cannot find any usage of log4j 2.x anywhere, we have no plans to do an emergency release at this time.
