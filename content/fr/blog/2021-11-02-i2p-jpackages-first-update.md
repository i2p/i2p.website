---
title: "Les Jpackages I2P reçoivent leur première mise à jour"
date: 2021-11-02
author: "idk"
description: "De nouveaux paquets, plus faciles à installer, atteignent un nouveau jalon"
categories: ["general"]
API_Translate: vrai
---

Il y a quelques mois, nous avons publié de nouveaux paquets dont nous espérions qu’ils aideraient à intégrer de nouvelles personnes au réseau I2P en rendant l’installation et la configuration d’I2P plus faciles pour davantage de personnes. Nous avons supprimé des dizaines d’étapes du processus d’installation en passant d’une JVM externe à un Jpackage, créé des paquets standard pour les systèmes d’exploitation ciblés et les avons signés de manière à ce que le système d’exploitation les reconnaisse afin de protéger l’utilisateur. Depuis, les routers basés sur jpackage ont franchi un nouveau jalon : ils s’apprêtent à recevoir leurs premières mises à jour incrémentielles. Ces mises à jour remplaceront le jpackage JDK 16 par un jpackage JDK 17 mis à jour et apporteront des correctifs pour quelques petits bogues que nous avons détectés après la publication.

## Mises à jour communes à Mac OS et Windows

Tous les programmes d'installation I2P jpackaged reçoivent les mises à jour suivantes :

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Veuillez mettre à jour dès que possible.

## Mises à jour de Jpackage pour I2P sous Windows

Les paquets destinés uniquement à Windows reçoivent les mises à jour suivantes :

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Pour la liste complète des modifications, consultez changelog.txt dans i2p.firefox

## Mises à jour de Jpackage pour I2P sur Mac OS

Les paquets réservés à Mac OS reçoivent les mises à jour suivantes :

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Pour un résumé du développement, voir les commits dans i2p-jpackage-mac.
