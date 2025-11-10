---
title: "Notes d'état d'I2P pour le 2006-01-10"
date: 2006-01-10
author: "jr"
description: "Mise à jour hebdomadaire portant sur les algorithmes de profilage du débit, les améliorations de l'affichage du blog de Syndie, l'avancement des connexions HTTP persistantes et le développement du gwebcache d'I2Phex"
categories: ["status"]
---

Salut tout le monde, on dirait que mardi est déjà de retour

* Index

1) État du réseau 2) Profilage du débit 3) blogs Syndie 4) connexions HTTP persistantes 5) gwebcache d'I2Phex 6) ???

* 1) Net status

La semaine passée a vu beaucoup de correctifs et d’améliorations entrer dans CVS, la build actuelle en étant à 0.6.1.8-11. Le réseau a été raisonnablement stable, même si des pannes chez différents fournisseurs de services I2P ont entraîné quelques ratés occasionnels. Nous nous sommes enfin débarrassés dans CVS du churn (renouvellement trop fréquent) des identités du router, qui était inutilement élevé, et zzz a proposé hier un nouveau correctif du noyau qui semble très prometteur, mais nous devrons attendre pour voir quel impact il aura. Deux autres gros chantiers de la semaine écoulée ont été le nouveau profilage de vitesse basé sur le débit, ainsi que des travaux majeurs sur la vue du blog de Syndie. Quant au moment où nous verrons la 0.6.1.9, elle devrait sortir plus tard cette semaine, au plus tard ce week-end. Restez à l’écoute des canaux habituels.

* 2) Throughput profiling

Nous avons testé quelques nouveaux algorithmes de profilage des pairs pour la surveillance du débit, mais au cours de la dernière semaine environ, il semble que nous nous soyons arrêtés sur un qui paraît plutôt bon. Essentiellement, il surveille le débit confirmé de tunnels individuels sur des périodes d'une minute, en ajustant en conséquence les estimations de débit pour les pairs. Il n'essaie pas de déterminer un débit moyen pour un pair, car cela est très compliqué, du fait que les tunnels incluent plusieurs pairs, ainsi que du fait que les mesures de débit confirmé nécessitent souvent plusieurs tunnels. À la place, il calcule un débit de pointe moyen - plus précisément, il mesure les trois débits les plus rapides que les tunnels du pair ont pu atteindre et en fait la moyenne.

L’essentiel est que ces taux, étant mesurés sur une minute entière, correspondent à des débits soutenus que le pair est capable de fournir, et puisque chaque pair est au moins aussi rapide que le débit mesuré de bout en bout, il est prudent de les marquer chacun comme étant aussi rapides. Nous avions essayé une autre variante sur ce point - mesurer le débit global d’un pair à travers des tunnels sur différentes périodes, ce qui fournissait des informations encore plus claires sur les débits de pointe, mais cela pénalisait fortement les pairs qui n’étaient pas déjà marqués comme "fast" (rapide), puisque ceux "fast" sont utilisés bien plus fréquemment (les tunnels client n’utilisent que des pairs "fast"). Le résultat de cette mesure de débit global était qu’elle recueillait d’excellentes données pour ceux qui étaient suffisamment sollicités, mais seuls les pairs "fast" étaient suffisamment sollicités et il y avait peu d’exploration efficace.

En utilisant des périodes d'une minute et le débit d'un tunnel individuel, cependant, cela semble donner des valeurs plus raisonnables. Nous verrons cet algorithme déployé dans la prochaine version.

* 3) Syndie blogs

Suite à certains retours, d'autres améliorations ont été apportées à la vue de blog de Syndie, lui donnant un caractère nettement différent de la vue en fils de discussion de type newsgroup/forum. En outre, une toute nouvelle fonctionnalité permet de définir des informations générales du blog via l'architecture Syndie existante. À titre d'exemple, consultez l'article de blog par défaut "about Syndie" :  http://syndiemedia.i2p.net/blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800001

Ce n’est qu’un aperçu de ce que nous pouvons faire. La prochaine version vous permettra de définir le logo de votre propre blog, vos propres liens (vers des blogs, des articles, des pièces jointes, et n’importe quelles URL externes), et, espérons-le, encore plus d’options de personnalisation. L’une de ces personnalisations consiste à associer des icônes par étiquette — j’aimerais fournir un jeu d’icônes par défaut à utiliser avec les étiquettes standard, mais les gens pourront définir des icônes pour leurs propres étiquettes à utiliser au sein de leur blog, et même remplacer les icônes par défaut pour les étiquettes standard (là encore, uniquement lorsque les gens consultent leur blog, bien entendu). Peut-être même une configuration de style pour afficher différemment les articles selon les étiquettes (bien sûr, seules des personnalisations de style très spécifiques seraient autorisées - pas d’exploits CSS arbitraires avec Syndie, merci bien :)

Il y a encore beaucoup de choses que j’aimerais faire avec la vue du blog et qui ne seront pas dans la prochaine version, mais cela devrait donner un bon coup d’élan pour amener les gens à jouer avec certaines de ses fonctionnalités, ce qui, je l’espère, vous permettra de me montrer ce dont *vous* avez besoin, plutôt que ce que je pense que vous voulez. Je suis peut‑être un bon développeur, mais je ne suis pas devin.

* 4) HTTP persistent connections

zzz est un acharné, je vous le dis. Il y a eu des progrès sur une fonctionnalité demandée depuis longtemps — la prise en charge des connexions HTTP persistantes, qui permet d’envoyer plusieurs requêtes HTTP sur un seul flux et de recevoir plusieurs réponses en retour. Je crois que quelqu’un l’a demandée pour la première fois il y a environ deux ans, et cela pourrait beaucoup aider pour certains types d’eepsite (I2P Site) ou pour l’outproxying (utilisation d’un proxy de sortie). Je sais que le travail n’est pas encore terminé, mais ça avance bien. Avec un peu de chance, zzz pourra nous donner une mise à jour de l’état d’avancement pendant la réunion.

* 5) I2Phex gwebcache

J’ai entendu dire qu’il y avait des progrès pour réintégrer la prise en charge de gwebcache dans I2Phex, mais je ne sais pas où cela en est pour le moment. Peut-être que Complication pourra nous donner une mise à jour à ce sujet ce soir ?

* 6) ???

Comme vous pouvez le voir, il se passe beaucoup de choses, mais s’il y a d’autres sujets que vous aimeriez aborder et discuter, passez à la réunion dans quelques minutes et faites signe. Au passage, un site sympa que je surveille ces derniers temps est http://freedomarchive.i2p/ (pour les paresseux qui n’ont pas installé I2P, vous pouvez utiliser l’inproxy de Tino via http://freedomarchive.i2p.tin0.de/). Dans tous les cas, on se retrouve dans quelques minutes.

=jr
