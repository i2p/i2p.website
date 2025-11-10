---
title: "Notes d'état I2P du 2004-10-12"
date: 2004-10-12
author: "jr"
description: "Mise à jour hebdomadaire de l'état d'I2P couvrant la sortie de la version 0.4.1.2, des expériences de limitation dynamique du débit, le développement de la bibliothèque de streaming pour la 0.4.2, et des discussions par e-mail"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de notre mise à jour hebdomadaire

## Index :

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

La nouvelle version 0.4.1.2 est sortie depuis quelques jours et les choses se passent globalement comme prévu - il y a toutefois eu quelques accrocs avec le nouveau composant watchdog, qui a tendance à tuer votre router lorsque la situation est mauvaise plutôt que de le redémarrer. Comme je l’ai mentionné plus tôt aujourd’hui, je cherche des personnes prêtes à utiliser le nouvel outil de journalisation des statistiques pour m’envoyer des données, donc votre aide à ce sujet serait grandement appréciée.

## 2) 0.4.1.3

Il y aura une autre version avant la sortie de la 0.4.2, car je veux que le réseau soit aussi solide que possible avant de passer à la suite. Ce que j’expérimente en ce moment est une limitation dynamique de la participation aux tunnels - en demandant aux routers de rejeter les requêtes de manière probabiliste s’ils sont saturés ou si leurs tunnels sont plus lents que d’habitude. Ces probabilités et ces seuils sont calculés dynamiquement à partir des statistiques conservées - si votre temps de test de tunnel sur 10 minutes est supérieur à votre temps de test de tunnel sur 60 minutes, acceptez la requête de tunnel avec une probabilité de 60minRate/10minRate (et si votre nombre actuel de tunnels est supérieur à votre nombre moyen de tunnels sur 60 minutes, acceptez-la avec p=60mRate/curTunnels).

Un autre mécanisme de limitation possible est de lisser la bande passante dans ce sens - en rejetant des tunnels de manière probabiliste lorsque notre utilisation de bande passante connaît des pics. Quoi qu'il en soit, l'objectif de tout cela est d'aider à répartir l'utilisation du réseau et à équilibrer les tunnels entre davantage de personnes. Le principal problème que nous avons rencontré avec l'équilibrage de charge a été un *excès* écrasant de capacité, et, de ce fait, aucun de nos déclencheurs "mince, on est lents, rejetons" n'a été activé. Ces nouveaux mécanismes probabilistes devraient, espérons-le, maintenir les changements rapides sous contrôle.

Je n’ai pas de plan précis quant au moment où la version 0.4.1.3 sortira — peut-être ce week-end. Les données que les gens envoient (ci-dessus) devraient aider à déterminer si cela en vaut la peine, ou s’il existe d’autres pistes plus intéressantes.

## 3) 0.4.2

Comme nous en avons discuté lors de la réunion de la semaine dernière, nous avons interverti les versions 0.4.2 et 0.4.3 - la 0.4.2 sera la nouvelle bibliothèque de streaming, et la 0.4.3 sera la mise à jour du tunnel.

Je réexamine la littérature sur la fonctionnalité de streaming de TCP et certains points soulèvent des préoccupations pour I2P. Plus précisément, notre temps aller-retour élevé nous incite à privilégier quelque chose comme XCP, et nous devrions probablement être assez agressifs avec diverses formes de notification explicite de congestion, bien que nous ne puissions pas tirer parti de quelque chose comme l’option Timestamp (option d’horodatage), puisque nos horloges peuvent être décalées jusqu’à une minute.

En outre, nous voudrons nous assurer que nous pouvons optimiser la streaming lib (bibliothèque de streaming) pour gérer les connexions de courte durée (dans lesquelles le TCP classique s'en sort très mal) - par exemple, je veux pouvoir envoyer de petites requêtes HTTP GET (<32KB) et de petites réponses (<32KB) en littéralement trois messages:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
Quoi qu’il en soit, on n’a pas encore écrit beaucoup de code à ce sujet, la partie protocole étant globalement de type TCP et les paquets ressemblant à une fusion de la proposition de human et de l’ancienne proposition. Si quelqu’un a des suggestions ou des idées, ou souhaite aider à l’implémentation, merci de prendre contact.

## 4) discussion par e-mail

Il y a eu quelques discussions intéressantes concernant le courriel dans (et en dehors d'I2P) - postman a mis en ligne un ensemble d'idées et cherche des suggestions. Il y a également eu des discussions connexes sur #mail.i2p. Peut-être pouvons-nous demander à postman de nous donner une mise à jour ?

## 5) ???

C’est à peu près tout pour le moment. Passe faire un tour à la réunion dans quelques minutes et apporte tes commentaires :)

=jr
