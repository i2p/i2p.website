---
title: "La naissance de Privacy Solutions"
date: 2014-08-15
author: "Meeh"
description: "Lancement de l’organisation"
categories: ["press"]
---

Bonjour à tous !

Aujourd’hui, nous annonçons le projet Privacy Solutions, une nouvelle organisation qui développe et maintient des logiciels I2P. Privacy Solutions comprend plusieurs nouvelles initiatives de développement conçues pour renforcer la vie privée, la sécurité et l’anonymat des utilisateurs, basées sur les protocoles et la technologie I2P.

Ces efforts comprennent :

1. The Abscond browser bundle.
2. The i2pd C++ router project.
3. The "BigBrother" I2P network monitoring project.
4. The Anoncoin crypto-coin project.
5. The Monero crypto-coin project.

Le financement initial de Privacy Solutions a été assuré par les soutiens des projets Anoncoin et Monero. Privacy Solutions est une organisation à but non lucratif basée en Norvège, enregistrée auprès des registres du gouvernement norvégien. (Un peu comme une 501(c)3 américaine.)

Privacy Solutions prévoit de demander un financement auprès du gouvernement norvégien pour la recherche sur les réseaux, en raison de BigBrother (nous reviendrons sur ce que c’est) et des cryptomonnaies conçues pour utiliser des réseaux à faible latence comme couche de transport principale. Nos recherches favoriseront des avancées dans les technologies logicielles en matière d’anonymat, de sécurité et de protection de la vie privée.

D’abord, quelques mots sur l’Abscond Browser Bundle. Il s’agissait au départ d’un projet mené par une seule personne, Meeh, mais des amis ont ensuite commencé à envoyer des correctifs; le projet cherche désormais à offrir le même accès facile à I2P que Tor avec leur browser bundle (ensemble navigateur préconfiguré). Notre première version n’est plus très loin : il ne reste que quelques tâches de scripts Gitian, y compris la configuration de la chaîne d’outils Apple. Mais encore une fois, nous ajouterons une surveillance avec PROCESS_INFORMATION (une structure C qui conserve des informations essentielles sur un processus) depuis l’instance Java pour contrôler I2P avant de le déclarer stable. I2pd remplacera également la version Java dès qu’il sera prêt, et il n’y a plus de raison d’inclure une JRE dans le bundle. Vous pouvez en lire davantage sur l’Abscond Browser Bundle à l’adresse https://hideme.today/dev

Nous souhaitons également vous informer de l'état actuel d'i2pd. I2pd prend désormais en charge le streaming bidirectionnel, ce qui permet d'utiliser non seulement HTTP, mais aussi des canaux de communication de longue durée. Le support IRC instantané a été ajouté. Les utilisateurs d'i2pd sont en mesure de l'utiliser de la même manière que Java I2P pour accéder au réseau IRC I2P. I2PTunnel est l'une des fonctionnalités clés du réseau I2P, permettant aux applications non I2P de communiquer de manière transparente. C'est pourquoi il s'agit d'une fonctionnalité vitale pour i2pd et de l'un des jalons clés.

Enfin, si vous êtes familier avec I2P, vous connaissez probablement Bigbrother.i2p, qui est un système de métriques que Meeh a créé il y a plus d’un an. Récemment, nous avons constaté que Meeh dispose en fait de 100Gb de données non dupliquées provenant des nœuds qui rapportent depuis le lancement initial. Cela sera également déplacé chez Privacy Solutions et réécrit avec un backend NSPOF (sans point de défaillance unique). Dans ce cadre, nous commencerons également à utiliser Graphite (http://graphite.wikidot.com/screen-shots). Cela nous donnera une excellente vue d’ensemble du réseau, sans problèmes de confidentialité pour nos utilisateurs finaux. Les clients filtrent toutes les données, à l’exception du pays, du router hash et du taux de réussite lors de la construction des tunnels. Le nom de ce service est, comme toujours, une petite blague de Meeh.

Nous avons légèrement raccourci les actualités ici ; si vous souhaitez davantage d'informations, veuillez visiter https://blog.privacysolutions.no/ Nous sommes encore en cours de construction et davantage de contenu arrivera !

Pour de plus amples informations, contactez : press@privacysolutions.no

Cordialement,

Mikal "Meeh" Villa
