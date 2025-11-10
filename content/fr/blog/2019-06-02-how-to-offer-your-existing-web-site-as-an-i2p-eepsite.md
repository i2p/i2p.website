---
title: "Comment proposer votre site Web existant en tant qu’eepSite I2P"
date: 2019-06-02
author: "idk"
description: "Proposer un miroir I2P"
categories: ["tutorial"]
---

Ce billet de blog vise à servir de guide général pour exploiter un miroir d’un service du clearnet sous la forme d’un eepSite. Il approfondit le billet de blog précédent à propos des tunnels I2PTunnel de base.

Malheureusement, il est probablement impossible de couvrir *complètement* tous les cas possibles consistant à rendre un site web existant disponible en tant qu'eepSite. Il existe tout simplement une trop grande diversité de logiciels côté serveur, sans parler des particularités pratiques propres à chaque déploiement de logiciel. Je vais plutôt essayer de présenter, aussi précisément que possible, le processus général de préparation d'un service en vue de son déploiement sur l'eepWeb ou d'autres services cachés.

Une grande partie de ce guide s’adressera au lecteur comme à un interlocuteur ; en particulier, pour être bien clair, je m’adresserai directement au lecteur (c.-à-d. en utilisant « vous » plutôt que « on ») et j’intitulerai fréquemment des sections par des questions que j’imagine que le lecteur pourrait se poser. Après tout, il s’agit d’un « processus » dans lequel un administrateur doit se considérer « impliqué », exactement comme pour l’hébergement de tout autre service.

**CLAUSES DE NON-RESPONSABILITÉ:**

Même si ce serait formidable, il m'est probablement impossible de fournir des instructions spécifiques pour chaque type de logiciel que l'on pourrait utiliser pour héberger des sites web. Par conséquent, ce tutoriel repose sur certaines hypothèses de la part de l'auteur et demande de l'esprit critique et du bon sens de la part du lecteur. Pour être clair, **j'ai supposé que la personne qui suit ce tutoriel exploite déjà un service clear-web (Internet public/clearnet) pouvant être relié à une identité ou à une organisation réelle** et se contente donc d'offrir un accès anonyme sans s'anonymiser elle-même.

Ainsi, **il ne tente absolument pas d’anonymiser** une connexion d’un serveur à un autre. Si vous souhaitez exploiter un nouveau service caché non corrélable qui héberge du contenu qui ne vous est pas lié, vous ne devriez pas le faire depuis votre propre serveur clearnet ni depuis votre domicile.
