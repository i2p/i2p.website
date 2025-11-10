---
title: "Notes d'état d'I2P du 2005-02-01"
date: 2005-02-01
author: "jr"
description: "Notes hebdomadaires sur l’état du développement d’I2P couvrant l’avancement du chiffrement du tunnel 0.5, un nouveau serveur NNTP et des propositions techniques"
categories: ["status"]
---

Salut tout le monde, c’est l’heure du point hebdo

* Index

1) statut 0.5 2) nntp 3) propositions techniques 4) ???

* 1) 0.5 status

Il y a eu beaucoup de progrès sur le front 0.5, avec une grosse série de commits hier. La majeure partie du router utilise désormais le nouveau tunnel encryption et le tunnel pooling [1], et cela fonctionne bien sur le réseau de test. Il reste encore quelques éléments clés à intégrer, et le code n’est évidemment pas rétrocompatible, mais j’espère que nous pourrons procéder à un déploiement à plus grande échelle dans le courant de la semaine prochaine.

Comme indiqué précédemment, la version 0.5 initiale fournira la base sur laquelle différentes stratégies de sélection/ordonnancement des pairs de tunnel pourront opérer.  Nous commencerons par un ensemble de base de paramètres configurables pour les pools exploratoires et clients, mais des versions ultérieures incluront probablement d'autres options pour différents profils d'utilisateurs.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

Comme mentionné sur le site de LazyGuy [2] et sur mon blog [3], nous avons un nouveau serveur NNTP opérationnel sur le réseau, accessible à l’adresse nntp.fr.i2p. Bien que LazyGuy ait lancé quelques scripts suck [4] (outil pour récupérer des groupes de discussion via NNTP) pour récupérer quelques listes depuis gmane, le contenu est essentiellement par, pour et concernant les utilisateurs d’I2P. jdot, LazyGuy et moi-même avons fait des recherches sur les lecteurs de news qui peuvent être utilisés en toute sécurité, et il semble exister des solutions assez simples. Voir mon blog pour des instructions sur l’utilisation de slrn [5] afin de lire et publier des news de manière anonyme.

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion et d’autres ont mis en ligne une série de RFC pour diverses questions techniques sur le wiki d’ugha [6] afin d’aider à approfondir certains des problèmes les plus difficiles au niveau client et application. Veuillez l’utiliser comme lieu pour discuter des questions de nommage, des mises à jour de SAM, des idées d’essaimage (swarming), et autres sujets du même ordre - lorsque vous y publiez, nous pouvons tous collaborer en un lieu qui nous est propre afin d’obtenir un meilleur résultat.

[6] http://ugha.i2p/I2pRfc

* 4) ???

C’est tout ce que j’ai pour le moment (tant mieux d’ailleurs, la réunion commence dans un instant). Comme toujours, postez vos idées quand et où vous voulez :)

=jr
