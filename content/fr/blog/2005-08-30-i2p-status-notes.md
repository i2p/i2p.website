---
title: "Notes d'état d'I2P du 2005-08-30"
date: 2005-08-30
author: "jr"
description: "Mise à jour hebdomadaire couvrant l’état du réseau 0.6.0.3 avec des problèmes de NAT, le déploiement floodfill du netDb et l’avancement de l’internationalisation de Syndie"
categories: ["status"]
---

Salut tout le monde, c'est de nouveau ce moment de la semaine

* Index

1) État du réseau 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

La 0.6.0.3 étant sortie depuis une semaine, les retours sont plutôt bons, bien que la journalisation et l’affichage aient été assez déroutants pour certains. À l’instant, I2P signale toutefois qu’un nombre important de personnes ont mal configuré leurs NAT ou leurs pare-feux - sur 241 pairs, 41 ont vu le statut passer à ERR-Reject, tandis que 200 ont été directement OK (lorsqu’un statut explicite peut être obtenu). Ce n’est pas idéal, mais cela a permis de mieux cibler ce qu’il reste à faire.

Depuis la publication, quelques correctifs pour des erreurs persistantes ont été apportés, portant le CVS HEAD actuel à 0.6.0.3-4, qui sera probablement publié en tant que 0.6.0.4 plus tard cette semaine.

* 2) floodfill netDb

Comme évoqué [1] sur mon blog [2], nous essayons un nouveau netDb (base de données du réseau) rétrocompatible qui traitera à la fois la situation de routes restreintes que nous observons (20 % des routers) et simplifiera un peu les choses. Le floodfill netDb est déployé dans le cadre de 0.6.0.3-4 sans aucune configuration supplémentaire et, en gros, fonctionne en interrogeant la floodfill db avant de revenir à la kademlia db existante. Si quelques personnes veulent aider à le tester, passez à 0.6.0.3-4 et faites un essai !

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

Le développement de Syndie progresse plutôt bien, avec une syndication distante complète opérationnelle et optimisée pour les besoins d'I2P (en minimisant le nombre de requêtes HTTP, en regroupant plutôt les résultats et les téléversements dans des requêtes HTTP POST multipart). La nouvelle syndication distante signifie que vous pouvez exécuter votre propre instance locale de Syndie, lire et publier hors ligne, puis, plus tard, synchroniser votre Syndie avec celle de quelqu'un d'autre - en récupérant tous les nouveaux billets et en téléversant les billets créés localement (soit en lot, par blog ou par billet).

Un site Syndie public est syndiemedia.i2p (également accessible sur le web à l'adresse http://syndiemedia.i2p.net/), dont les archives publiques sont accessibles à l'adresse http://syndiemedia.i2p/archive/archive.txt (pointez votre nœud Syndie vers cette URL pour le synchroniser). La 'front page' sur ce syndiemedia a été filtrée pour n'inclure que mon blog, par défaut, mais vous pouvez toujours accéder aux autres blogs via le menu déroulant et modifier votre paramètre par défaut en conséquence. (avec le temps, le paramètre par défaut de syndiemedia.i2p évoluera vers un ensemble de billets et de blogs d'introduction, offrant un bon point d'entrée dans syndie).

Un effort encore en cours est l’internationalisation de la base de code de Syndie. J’ai modifié ma copie locale pour qu’elle fonctionne correctement avec tout contenu (n’importe quel jeu de caractères / paramètres régionaux / etc.) sur n’importe quelle machine (avec des jeux de caractères / paramètres régionaux potentiellement différents / etc.), en fournissant des données propres afin que le navigateur de l’utilisateur puisse les interpréter correctement. Cependant, j’ai rencontré des problèmes avec un composant Jetty utilisé par Syndie, car leur classe chargée de traiter les requêtes multipart (multipart/form-data) internationalisées n’est pas sensible au jeu de caractères. Pas encore ;)

Quoi qu’il en soit, cela signifie qu’une fois la partie internationalisation réglée, le contenu et les blogs seront rendus et modifiables dans toutes les langues (mais pas encore traduits, bien sûr). D’ici là, le contenu créé pourrait se retrouver foiré une fois l’internationalisation terminée (puisqu’il y a des chaînes UTF-8 à l’intérieur des zones de contenu signées). Mais quand même, n’hésitez pas à bidouiller, et j’espère pouvoir terminer tout ça ce soir ou demain.

De plus, parmi les idées encore à l’horizon pour SML [3] figure une balise [torrent attachment="1"]my file[/torrent] qui offrirait un moyen en un clic de lancer le torrent joint dans le client BT préféré des utilisateurs (susibt, i2p-bt, azneti2p, ou même un client BT non-I2P). Existe-t-il une demande pour d’autres types de hooks (points d’intégration) (par exemple une balise [ed2k] ?), ou bien les gens ont-ils des idées complètement différentes et folles pour diffuser du contenu dans Syndie ?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

Bref, il se passe énormément de choses, alors rejoignez la réunion dans 10 minutes sur irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p ou freenode.net !

=jr
