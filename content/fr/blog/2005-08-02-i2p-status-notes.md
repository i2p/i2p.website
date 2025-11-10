---
title: "Notes d'état d'I2P du 2005-08-02"
date: 2005-08-02
author: "jr"
description: "Mise à jour tardive couvrant le statut de la version 0.6, le système PeerTest, les introductions SSU, des correctifs de l’interface web d’I2PTunnel, et mnet sur I2P"
categories: ["status"]
---

Salut tout le monde, des notes en retard aujourd'hui,

* Index:

1) Statut 0.6 2) PeerTest 3) introductions SSU 4) interface web d'I2PTunnel 5) mnet via i2p 6) ???

* 1) 0.6 status

Comme vous l'avez tous constaté, nous avons publié la version 0.6 il y a quelques jours et, dans l'ensemble, les choses se passent plutôt bien. Certaines des améliorations du transport depuis la 0.5.* ont mis en évidence des problèmes avec l'implémentation de netDb, mais des correctifs pour une bonne partie de cela sont actuellement en test (sous la forme de la build 0.6-1) et seront déployés sous la version 0.6.0.1 très prochainement. Nous avons également rencontré des problèmes avec différentes configurations de NAT et de pare-feu, ainsi que des problèmes de MTU chez certains utilisateurs - des problèmes qui n'étaient pas présents dans le réseau de test plus restreint en raison du nombre plus faible de testeurs. Des solutions de contournement ont été ajoutées pour les cas les plus problématiques, mais nous avons une solution à long terme qui arrive bientôt - peer tests (tests entre pairs).

* 2) PeerTest

Avec la version 0.6.1, nous allons déployer un nouveau système pour tester et configurer de manière collaborative les adresses IP publiques et les ports. Celui-ci est intégré au cœur du protocole SSU et sera rétrocompatible. Essentiellement, il permet à Alice de demander à Bob quelle est son adresse IP publique et quel est son numéro de port, puis à Bob de demander à Charlie de confirmer qu’elle est correctement configurée, ou de déterminer quelle limitation empêche le bon fonctionnement. Cette technique n’a rien de nouveau sur le Net, mais c’est un ajout récent à la base de code d’I2P et elle devrait éliminer la plupart des erreurs de configuration courantes.

* 3) SSU introductions

Comme décrit dans la spécification du protocole SSU, une fonctionnalité permettra aux personnes derrière des pare-feux et des NAT (traduction d’adresses réseau) de participer pleinement au réseau, même si elles ne pourraient autrement pas recevoir de messages UDP non sollicités. Cela ne fonctionnera pas dans toutes les situations possibles, mais couvrira la plupart.

Il existe des similitudes entre les messages décrits dans la spécification SSU et les messages nécessaires pour le PeerTest (test de pair), donc peut-être que, lorsque la spécification sera mise à jour pour inclure ces messages, nous pourrons faire passer les introductions en même temps que les messages PeerTest. Quoi qu’il en soit, nous déploierons ces introductions dans la 0.6.2, et cela sera également rétrocompatible.

* 4) I2PTunnel web interface

Certaines personnes ont remarqué et déposé des rapports concernant diverses anomalies sur l’interface web d’I2PTunnel, et smeghead a commencé à préparer les correctifs nécessaires — peut‑être peut‑il expliquer ces mises à jour plus en détail, ainsi que fournir une estimation de leur date de disponibilité ?

* 5) mnet over i2p

Bien que je n’aie pas été présent sur le canal pendant que les discussions avaient lieu, à la lecture des journaux il semble qu’icepick ait réalisé quelques hacks pour faire tourner mnet par-dessus i2p - permettant au stockage de données distribué mnet d’offrir une publication de contenu résiliente avec un fonctionnement anonyme. Je ne connais pas très bien l’état d’avancement sur ce front, mais il semble qu’icepick fasse de bons progrès pour s’intégrer à I2P via SAM et twisted, mais peut-être qu’icepick pourra nous en dire davantage ?

* 6) ???

Ok, il se passe beaucoup plus de choses que ce qui est décrit ci-dessus, mais je suis déjà en retard, donc je suppose que je devrais arrêter d’écrire et envoyer ce message. Je pourrai me connecter un peu ce soir, donc si quelqu’un est dans les parages, on pourrait se retrouver vers 21 h 30 (quand vous verrez ceci ;) sur #i2p sur les serveurs IRC habituels {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net}.

Merci de votre patience et de votre aide pour faire avancer les choses !

=jr
