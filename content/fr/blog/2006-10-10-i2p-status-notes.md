---
title: "Notes sur l'état d'I2P du 2006-10-10"
date: 2006-10-10
author: "jr"
description: "Sortie de la version 0.6.1.26 avec des retours positifs, Syndie 0.910a se rapproche de la version 1.0, et évaluation du contrôle de version distribué pour Syndie"
categories: ["status"]
---

Salut tout le monde, brèves notes de statut cette semaine

* Index

1) 0.6.1.26 et état du réseau 2) État du développement de Syndie 3) Contrôle de version distribué revisité 4) ???

* 1) 0.6.1.26 and network status

L’autre jour, nous avons publié une nouvelle version 0.6.1.26, incluant de nombreuses améliorations d’i2psnark de zzz et quelques nouvelles vérifications de sécurité NTP de Complication, et les retours ont été positifs. Le réseau semble croître légèrement sans nouveaux effets étranges, bien que certaines personnes aient encore des difficultés à établir leurs tunnels (comme cela a toujours été le cas).

* 2) Syndie development status

De plus en plus d’améliorations arrivent, la version alpha actuelle en est à 0.910a. La liste des fonctionnalités prévues pour la 1.0 est pratiquement complète, donc pour l’instant, c’est surtout des corrections de bogues et de la documentation. Passez faire un tour sur #i2p si vous voulez aider à tester :)

De plus, il y a eu quelques discussions sur le canal à propos de la conception de la Syndie GUI (interface graphique) - meerboop a proposé quelques idées sympas et travaille à les documenter. La Syndie GUI est le composant principal de la version Syndie 2.0, donc plus vite nous mettrons cela en route, plus vite nous dominerons le monde^W^W^W^W pourrons diffuser Syndie auprès des masses qui ne se doutent de rien.

Il y a aussi une nouvelle proposition sur mon blog Syndie concernant le suivi des bogues et des demandes de fonctionnalités en utilisant Syndie lui-même. Pour faciliter l'accès, j'ai mis en ligne une exportation en texte brut de cet article sur le Web - la page 1 se trouve à <http://dev.i2p.net/~jrandom/bugsp1.txt> et la page 2 se trouve à <http://dev.i2p.net/~jrandom/bugsp2.txt>

* 3) Distributed version control revisited

L’une des choses qu’il reste à déterminer pour Syndie est le système public de contrôle de versions à utiliser, et comme mentionné précédemment, des fonctionnalités distribuées et hors ligne sont nécessaires. J’ai passé en revue la demi-douzaine environ de solutions open source disponibles (darcs, mercurial, git/cogito, monotone, arch, bzr, codeville), en épluchant leur documentation, en les essayant et en discutant avec leurs développeurs. À l’heure actuelle, monotone et bzr semblent être les meilleurs en termes de fonctionnalités et de sécurité (avec des dépôts non fiables, nous avons besoin d’une cryptographie forte pour nous assurer que nous ne récupérons que des modifications authentiques), et l’intégration étroite de la cryptographie dans monotone semble très attrayante. Je suis toutefois encore en train de parcourir les plusieurs centaines de pages de documentation, mais d’après mes échanges avec les développeurs de monotone, ils semblent faire les choses dans les règles de l’art.

Bien sûr, quel que soit le DVCS (système de contrôle de versions distribué) que nous finirons par adopter, toutes les versions seront disponibles au format tar simple, et les correctifs seront acceptés pour examen au format diff -uw simple. Cela dit, pour ceux qui envisagent de participer au développement, j’aimerais beaucoup connaître vos avis et préférences.

* 4) ???

Comme vous pouvez le voir, il se passe beaucoup de choses, comme toujours. La discussion s'est également poursuivie dans le fil "solve world hunger" sur le forum, alors allez-y jeter un œil à <http://forum.i2p.net/viewtopic.php?t=1910>

Si vous avez autre chose à discuter, passez faire un tour sur #i2p pour notre réunion des développeurs ce soir, ou publiez sur le forum ou la liste de diffusion !

=jr
