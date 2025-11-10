---
title: "I2P Jpackages get their First Update"
date: 2021-11-02
author: "idk"
description: "New, easier-to-install packages reach a new milestone"
categories: ["general"]
---

A few months ago we released new packages which we hoped would help with onboarding new people to the I2P network by making the installation and configuration of I2P easier for more people. We removed dozens of steps from the installation process by switching from an external JVM to a Jpackage, built standard packages for target operating systems, and signed them in a way the operating system would recognize to keep the user secure. Since then, the jpackage routers have reached a new milestone, they are about to recieve their first incremental updates. These updates will replace the JDK 16 jpackage with an updated JDK 17 jpackage and provide fixes for some small bugs which we caught after the release.

## Updates common to Mac OS and Windows

All jpackaged I2P installers recieve the following updates:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Please update as soon as possible.

## I2P Windows Jpackage Updates

Windows only packages recieve the following updates:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

For a full list of changes see the changelog.txt in i2p.firefox

## I2P Mac OS Jpackage Updates

Mac OS only packages recieve the following updates:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

For a summary of development see the checkins in i2p-jpackage-mac
