---
title: "Notes d'état I2P du 2005-08-23"
date: 2005-08-23
author: "jr"
description: "Mise à jour hebdomadaire couvrant les améliorations de la version 0.6.0.3, l’état du réseau Irc2P, l’interface web susibt pour i2p-bt et le blogging sécurisé avec Syndie"
categories: ["status"]
---

Salut à tous, c'est à nouveau l'heure des notes de statut hebdomadaires

* Index

1) 0.6.0.3 statut 2) statut IRC 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

Comme mentionné l’autre jour [1], nous avons une nouvelle version 0.6.0.3 disponible, prête à être utilisée. C’est une nette amélioration par rapport à la version 0.6.0.2 (il n’est pas rare de passer plusieurs jours sans déconnexion sur irc - j’ai eu des temps de fonctionnement de 5 jours, interrompus par une mise à jour), mais il y a quelques points à noter. Cela dit, ce n’est pas toujours le cas - les personnes ayant des connexions Internet lentes rencontrent des difficultés, mais c’est un progrès.

Une question (très) fréquente est revenue au sujet du code de test des pairs-"Pourquoi indique-t-il Status: Unknown ?" Unknown est *tout à fait normal* - ce n'est PAS le signe d'un problème. De plus, s'il passe parfois entre "OK" et "ERR-Reject", cela NE veut PAS dire que tout va bien - si vous voyez ERR-Reject à un moment, cela signifie qu'il est très probable que vous ayez un problème de NAT ou de pare-feu. Je sais que c'est déroutant, et il y aura plus tard une version avec un affichage du statut plus clair (et une résolution automatique, quand c'est possible), mais pour l'instant, ne soyez pas surpris si je vous ignore quand vous dites "omg c'est cassé!!!11 le statut est Unknown !" ;)

(La cause du nombre excessif de valeurs d’état "Unknown" est que nous ignorons les tests entre pairs où "Charlie" [2] est un pair avec lequel nous avons déjà une session SSU, puisque cela implique que "Charlie" pourra traverser notre NAT même si notre NAT est défaillant)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

Comme mentionné ci-dessus, les opérateurs d'Irc2P ont fait un excellent travail avec leur réseau, car la latence a fortement diminué et la fiabilité a nettement augmenté - je n'ai pas vu de netsplit (séparation du réseau) depuis des jours. Il y a aussi un nouveau serveur IRC sur ce réseau, ce qui nous en fait 3 - irc.postman.i2p, irc.arcturus.i2p, et irc.freshcoffee.i2p. Peut-être que l'un des membres d'Irc2P pourra nous faire un point sur l'avancement de leurs travaux pendant la réunion ?

* 3) susibt

susi23 (bien connue pour susimail) est de retour avec deux outils liés à bt - susibt [3] et un nouveau bot de tracker [4]. susibt est une application web (facilement déployable dans votre instance i2p jetty) pour gérer le fonctionnement d’i2p-bt. Comme le dit son site :

SusiBT est une interface web pour i2p-bt. Elle s’intègre à votre router i2p et permet des téléversements et téléchargements automatiques, reprend après redémarrage et offre certaines fonctionnalités de gestion comme le téléversement et le téléchargement de fichiers. Les versions ultérieures de l’application prendront en charge la génération et le téléversement automatiques de fichiers torrent.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

Est-ce que j’entends un « w00t » ?

* 4) Syndie

Comme mentionné sur la liste de diffusion et sur le canal, nous avons une nouvelle application cliente pour le blogging/la distribution de contenu sécurisés et authentifiés. Avec Syndie, la question « est-ce que ton eepsite(I2P Site) est en ligne » disparaît, puisqu’on peut lire le contenu même lorsque le site est indisponible, et Syndie évite tous les problèmes épineux inhérents aux réseaux de distribution de contenu en se concentrant sur l’interface. Quoi qu’il en soit, c’est encore largement en cours de développement, mais si certains veulent s’y mettre et l’essayer, il existe un nœud Syndie public à http://syndiemedia.i2p/ (également accessible sur le web à http://66.111.51.110:8000/). N’hésitez pas à y créer un blog, ou, si vous vous sentez aventureux, à publier des commentaires/suggestions/préoccupations ! Bien sûr, les correctifs sont les bienvenus, tout comme les suggestions de fonctionnalités, alors lâchez-vous.

* 5) ???

Dire qu’il se passe beaucoup de choses est un euphémisme... au-delà de ce qui précède, je travaille sur quelques améliorations du contrôle de congestion de SSU (-1 est déjà dans cvs), de notre limiteur de bande passante, et de la netDb (pour l’inaccessibilité occasionnelle de sites), ainsi que sur le débogage du problème de CPU signalé sur le forum. Je suis sûr que d’autres bidouillent aussi des trucs sympas à annoncer, alors j’espère qu’ils passeront à la réunion de ce soir pour se lâcher :)

Bref, on se retrouve ce soir à 20 h GMT sur #i2p, sur les serveurs habituels !

=jr
