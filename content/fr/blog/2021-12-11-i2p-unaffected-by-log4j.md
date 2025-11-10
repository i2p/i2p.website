---
title: "I2P n'est pas affecté par la vulnérabilité log4j"
date: 2021-12-11
author: "idk, zzz"
description: "I2P n'utilise pas log4j et n'est donc pas affecté par CVE-2021-44228"
categories: ["security"]
API_Translate: vrai
---

I2P n’est pas affecté par la vulnérabilité 0‑day de log4j publiée hier, CVE‑2021‑44228. I2P n’utilise pas log4j pour la journalisation ; nous avons toutefois aussi vérifié nos dépendances pour un éventuel usage de log4j, notamment jetty. Cette vérification n’a révélé aucune vulnérabilité.

Il était également important de vérifier l’ensemble de nos plugins. Les plugins peuvent embarquer leurs propres systèmes de journalisation, y compris log4j. Nous avons constaté que la plupart des plugins n’utilisent pas non plus log4j, et que ceux qui l’utilisent n’emploient pas une version vulnérable de log4j.

Nous n'avons trouvé aucune dépendance, aucun plugin ni aucune application vulnérable.

Nous fournissons un fichier log4j.properties avec jetty pour les plugins qui introduisent log4j. Ce fichier n’a d’effet que sur les plugins qui utilisent la journalisation log4j en interne. Nous avons intégré la mesure d’atténuation recommandée dans le fichier log4j.properties. Les plugins qui activent log4j s’exécuteront avec la fonctionnalité vulnérable désactivée. Comme nous n’avons trouvé aucune utilisation de log4j 2.x, nous n’envisageons pas de publier une version d’urgence pour le moment.
