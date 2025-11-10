---
title: "Notes de statut d'I2P pour le 2004-07-20"
date: 2004-07-20
author: "jr"
description: "Mise à jour hebdomadaire du statut couvrant la publication de la version 0.3.2.3, les modifications de capacité, les mises à jour du site web et les considérations de sécurité"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, et la feuille de route**

Après la publication de la version 0.3.2.3 la semaine dernière, vous avez fait un excellent travail de mise à jour - il ne reste plus que deux retardataires maintenant (l’un en 0.3.2.2 et l’autre bien en arrière, en 0.3.1.4 :). Ces derniers jours, le réseau a été plus fiable que d’habitude - les gens restent sur irc.duck.i2p pendant des heures d’affilée, les téléchargements de fichiers volumineux depuis des eepsites(I2P Sites) réussissent, et l’accessibilité générale des eepsite(I2P Site) est plutôt bonne. Comme cela se passe bien et que je veux vous maintenir sur le qui-vive, j’ai décidé de changer quelques concepts fondamentaux et nous les déploierons dans une version 0.3.3 d’ici un jour ou deux.

Comme quelques personnes ont commenté notre calendrier, se demandant si nous allions respecter les dates que nous avions affichées, j’ai décidé qu’il valait probablement mieux mettre à jour le site web pour refléter la feuille de route que j’ai dans mon palmpilot, donc je l’ai fait [1]. Les dates ont été repoussées et certains éléments ont été déplacés, mais le plan reste le même que celui dont nous avons discuté le mois dernier [2].

0.4 satisfera les quatre critères de publication mentionnés (fonctionnel, sécurisé, anonyme et évolutif), mais avant 0.4.2, peu de personnes derrière des NAT et des pare-feux pourront participer, et avant 0.4.3 il y aura une limite supérieure effective à la taille du réseau en raison du surcoût lié au maintien d’un grand nombre de connexions TCP avec d’autres routers.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

Au cours de la dernière semaine environ, les gens sur #i2p m’ont entendu occasionnellement râler sur le fait que nos classements de fiabilité sont totalement arbitraires (et les difficultés que cela a causées dans les quelques dernières versions). Nous nous sommes donc complètement débarrassés de la notion de fiabilité, en la remplaçant par une mesure de capacité - "combien un pair peut-il faire pour nous ?" Cela a eu des effets en cascade dans tout le code de sélection et de profilage des pairs (et évidemment sur la console du router), mais à part cela, il n’y a pas eu beaucoup de changements.

Plus d’informations sur ce changement sont disponibles sur la page révisée de sélection des pairs [3], et lorsque la version 0.3.3 sera publiée, vous pourrez en constater l’impact par vous-mêmes (je fais des essais depuis quelques jours, en ajustant quelques paramètres, etc.).

[3] http://www.i2p.net/redesign/how_peerselection

**3) mises à jour du site web**

Au cours de la semaine écoulée, nous avons beaucoup avancé sur la refonte du site web [4] - en simplifiant la navigation, en nettoyant certaines pages clés, en important du contenu ancien et en rédigeant quelques nouvelles entrées [5]. Nous sommes presque prêts à mettre le site en ligne, mais il reste encore quelques tâches à accomplir.

Plus tôt aujourd'hui, duck a parcouru le site et a dressé l'inventaire des pages qui nous manquent, et après les mises à jour de cet après-midi, il reste quelques problèmes en suspens; j'espère que nous pourrons soit les traiter, soit trouver des volontaires pour s'y atteler :

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Pour le reste, je pense que le site est presque prêt à être mis en production. Quelqu’un a-t-il des suggestions ou des préoccupations à cet égard ?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) attaques et défenses**

Connelly a récemment proposé quelques nouvelles approches pour chercher des failles dans la sécurité et l’anonymat du réseau et, ce faisant, il a trouvé des moyens d’améliorer les choses. Même si certains aspects des techniques qu’il a décrites ne s’appliquent pas vraiment à I2P, peut‑être que vous y verrez des pistes pour les approfondir et attaquer le réseau encore davantage ? Allez, tentez le coup :)

**5) ???**

C'est à peu près tout ce dont je me souviens avant la réunion de ce soir - n'hésitez pas à soulever tout ce que j'ai pu oublier. Bref, on se retrouve sur #i2p dans quelques minutes.

=jr
