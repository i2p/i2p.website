---
title: "Notes de statut I2P du 2005-01-18"
date: 2005-01-18
author: "jr"
description: "Notes hebdomadaires sur l'état du développement d'I2P couvrant l'état du réseau, la conception du routage de tunnel 0.5, i2pmail.v2 et un correctif de sécurité pour azneti2p_0.2"
categories: ["status"]
---

Salut à tous, c’est l’heure de la mise à jour hebdomadaire

* Index

1) Statut du réseau 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

Hmm, pas grand-chose à signaler ici - tout fonctionne toujours comme la semaine dernière, la taille du réseau est toujours assez similaire, peut-être un peu plus grande. Quelques nouveaux sites intéressants font leur apparition - voir le forum [1] et orion [2] pour plus de détails.

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

Grâce à l’aide de postman, dox, frosk et cervantes (et de tous ceux qui ont fait transiter des données en tunnel via leurs routers ;), nous avons collecté une journée entière de statistiques sur la taille des messages [3]. On y trouve deux séries de statistiques - la hauteur et la largeur du zoom. Cela a été motivé par le désir d’explorer l’impact de différentes stratégies de bourrage des messages sur la charge du réseau, comme expliqué [4] dans l’un des brouillons du tunnel routing 0.5. (ooOOoo jolies images).

La partie inquiétante de ce que j’ai découvert en les examinant, c’est qu’en utilisant des seuils de padding (remplissage) assez simples ajustés manuellement, le fait de caler le padding sur ces tailles fixes conduirait malgré tout à plus de 25 % de bande passante gaspillée.  Ouais, je sais, on ne va pas faire ça. Peut-être que vous pourrez trouver quelque chose de mieux en fouillant dans ces données brutes.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

En fait, ce lien [4] nous mène à l’état des plans 0.5 pour le routage des tunnels. Comme Connelly l’a indiqué [5], il y a eu beaucoup de discussions récemment sur IRC au sujet de certains brouillons, avec polecat, bla, duck, nickster, detonate et d’autres qui ont apporté des suggestions et des questions fouillées (ok, et des sarcasmes ;). Après un peu plus d’une semaine, nous avons mis au jour une vulnérabilité potentielle dans [4], impliquant un adversaire qui parvenait d’une manière ou d’une autre à prendre le contrôle de la passerelle du tunnel entrant, et contrôlait également l’un des autres pairs plus loin dans ce tunnel. Bien que, dans la plupart des cas, cela ne suffirait pas en soi à exposer le point terminal, et qu’il serait difficile à réaliser d’un point de vue probabiliste à mesure que le réseau se développe, ça craint quand même (tm).

C'est là qu'intervient [6].  Cela élimine ce problème, nous permet d'avoir des tunnels de n'importe quelle longueur et résout la faim dans le monde [7].  Cela ouvre toutefois un autre problème, où un attaquant pourrait créer des boucles dans le tunnel, mais d'après une suggestion [8] que Taral a faite l'année dernière concernant les session tags (étiquettes de session) utilisés avec ElGamal/AES, nous pouvons minimiser les dommages causés en utilisant une série de générateurs de nombres pseudo-aléatoires synchronisés [9].

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] Devinez quelle affirmation est fausse ? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

Ne vous inquiétez pas si ce qui précède vous semble confus - vous voyez les dessous de problèmes de conception assez coriaces que nous sommes en train de démêler au grand jour. Si ce qui précède *ne vous semble pas* confus, n'hésitez pas à nous contacter, car nous sommes toujours à la recherche de nouvelles têtes pour décortiquer tout ça :)

Quoi qu'il en soit, comme je l'ai mentionné sur la liste [10], ensuite j'aimerais mettre en œuvre la deuxième stratégie [6] pour passer au crible les derniers détails. Le plan pour 0.5 est actuellement de regrouper toutes les modifications incompatibles avec les versions antérieures - le nouveau chiffrement des tunnels, etc - et de publier cela sous la version 0.5.0, puis, une fois que cela se sera stabilisé sur le réseau, de passer aux autres éléments de 0.5 [11], comme l'ajustement de la stratégie de pooling (mise en pool) telle que décrite dans les propositions, et de le publier sous la version 0.5.1. J'espère que nous pourrons encore publier la 0.5.0 d'ici la fin du mois, mais on verra.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

L’autre jour, postman a publié un projet de plan d’action pour l’infrastructure de messagerie de nouvelle génération [12], et ça a l’air sacrément cool. Bien sûr, on peut toujours imaginer encore plus de fonctionnalités, mais son architecture est vraiment réussie à bien des égards. Jetez un œil à ce qui a été documenté jusqu’à présent [13], et contactez postman pour lui faire part de vos idées !

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

Comme je l’ai indiqué sur la liste [14], le plug-in azneti2p d’origine pour azureus présentait un bogue grave affectant l’anonymat. Le problème, avec des torrents mixtes où certains utilisateurs sont anonymes et d’autres ne le sont pas, était que les utilisateurs anonymes contactaient les utilisateurs non anonymes /directement/ plutôt que via I2P. Paul Gardner et le reste des développeurs d’azureus ont été très réactifs et ont publié un correctif immédiatement. Le problème que j’ai observé n’est plus présent dans azureus v. 2203-b12 + azneti2p_0.2.

Nous n’avons toutefois pas procédé à un audit du code pour examiner d’éventuels problèmes d’anonymat, donc "à vos risques et périls" (d’un autre côté, nous disons la même chose à propos d’I2P avant la version 1.0). Si vous êtes partant, je sais que les développeurs d’Azureus apprécieraient davantage de retours et de rapports de bogues concernant le plugin. Nous tiendrons bien sûr tout le monde informé si nous découvrons d’autres problèmes.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Il se passe beaucoup de choses, comme vous pouvez le voir. Je pense que c’est à peu près tout ce que j’avais à aborder, mais venez à la réunion dans 40 minutes s’il y a autre chose dont vous souhaiteriez discuter (ou si vous voulez simplement râler à propos de ce qui précède).

=jr
