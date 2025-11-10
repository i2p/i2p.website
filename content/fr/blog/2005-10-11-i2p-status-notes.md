---
title: "Notes de statut I2P du 2005-10-11"
date: 2005-10-11
author: "jr"
description: "Mise à jour hebdomadaire couvrant le succès de la version 0.6.1.2, un nouveau proxy I2PTunnelIRCClient pour filtrer les messages IRC non sûrs, l’interface en ligne de commande de Syndie et la conversion RSS-to-SML, ainsi que les plans d’intégration d’I2Phex"
categories: ["status"]
---

Salut tout le monde, c’est encore mardi

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Stego (stéganographie) et darknets (à propos d’une flamewar) 6) ???

* 1) 0.6.1.2

La version 0.6.1.2 de la semaine dernière s’est jusqu’à présent plutôt bien passée - 75 % du réseau a effectué la mise à niveau, HTTP POST fonctionne bien, et la streaming lib (bibliothèque de streaming) achemine les données de façon raisonnablement efficace (la réponse complète à une requête HTTP est souvent reçue en un seul aller-retour de bout en bout). Le réseau a aussi un peu grandi - les chiffres stables semblent se situer autour de 400 pairs, bien qu’il ait encore bondi jusqu’à 600-700 avec le churn (rotation des pairs) pendant le pic de la mention sur digg/gotroot [1] durant le week-end.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (oui, un article vraiment ancien, je sais, mais quelqu'un l'a retrouvé)

Depuis la sortie de la 0.6.1.2, encore d'autres améliorations ont été ajoutées - la cause des récents netsplits (scissions du réseau) d'irc2p a été trouvée (et corrigée), et des améliorations assez conséquentes ont été apportées à la transmission des paquets de SSU (permettant d'économiser plus de 5 % des paquets). Je ne sais pas exactement quand la 0.6.1.3 sortira, mais peut-être plus tard cette semaine. On verra.

* 2) I2PTunnelIRCClient

L'autre jour, après quelques discussions, dust a rapidement développé une nouvelle extension pour I2PTunnel - le proxy "ircclient". Il fonctionne en filtrant le contenu envoyé et reçu entre le client et le serveur via I2P, en supprimant les messages IRC dangereux et en réécrivant ceux qui doivent être ajustés. Après quelques tests, le résultat est très convaincant, et dust l'a intégré à I2PTunnel et il est désormais proposé aux utilisateurs via l'interface web. Il est très appréciable que les membres d'irc2p aient corrigé leurs serveurs IRC pour rejeter les messages dangereux, mais nous n'avons désormais plus besoin de leur faire confiance pour le faire - l'utilisateur local a le contrôle de son propre filtrage.

L'utiliser est assez simple - au lieu de créer un "Client proxy" pour IRC comme auparavant, créez simplement un "IRC proxy". Si vous souhaitez convertir votre "Client proxy" existant en "IRC proxy", vous pouvez (aïe) modifier le fichier i2ptunnel.config, en changeant "tunnel.1.type=client" en "tunnel.1.ircclient" (ou quel que soit le numéro approprié pour votre proxy).

Si tout se passe bien, cela sera défini comme le type de proxy I2PTunnel par défaut pour les connexions IRC dans la prochaine version.

Beau travail dust, merci !

* 3) Syndie

La fonctionnalité de syndication planifiée de Ragnarok semble bien fonctionner, et depuis que la 0.6.1.2 est sortie, deux nouvelles fonctionnalités sont arrivées - j'ai ajouté une nouvelle CLI (interface en ligne de commande) simplifiée pour publier dans Syndie [2], et dust (youpi dust!) a rapidement écrit du code pour extraire du contenu d'un flux RSS/Atom, récupérer toutes les enclosures (fichiers joints) ou images qui y sont référencées, et convertir le contenu RSS en SML (!!!) [3][4].

Les implications de ces deux éléments réunis devraient être claires. Plus d'informations lorsqu'il y en aura.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (nous l'intégrerons dans CVS sous peu)

* 4) I2Phex

Selon les retours, I2Phex fonctionne plutôt bien, mais des problèmes persistent au fil du temps. Une discussion a eu lieu sur le forum [5] concernant la marche à suivre, et GregorK, le développeur principal de Phex, est même intervenu pour soutenir la réintégration des fonctionnalités d’I2Phex dans Phex (ou au moins pour que la version principale de Phex propose une interface de plugin simple pour la couche de transport).

Ce serait vraiment génial, car cela signifierait beaucoup moins de code à maintenir, et nous bénéficierions en plus du travail de l’équipe Phex pour améliorer la base de code. Cependant, pour que cela fonctionne, nous avons besoin que des hackers se manifestent et prennent en charge la migration. Le code d’I2Phex montre assez clairement où sirup a modifié des choses, donc ça ne devrait pas être trop difficile, mais ce n’est probablement pas tout à fait trivial non plus ;)

Je n’ai pas vraiment le temps de m’en occuper tout de suite, mais passez sur le forum si vous voulez aider.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

La liste de diffusion [6] a été assez active dernièrement avec des discussions concernant la stéganographie et les darknets. Le sujet s’est en grande partie déplacé vers la liste technique de Freenet [7] sous l'objet "I2P conspiracy theories flamewar", mais la discussion se poursuit.

Je ne suis pas sûr d’avoir beaucoup à ajouter qui ne fasse pas déjà partie des messages eux-mêmes, mais certaines personnes ont mentionné que la discussion les avait aidées à mieux comprendre I2P et Freenet, donc ça vaut peut-être le coup d’y jeter un œil. Ou peut-être pas ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

Comme vous pouvez le voir, il se passe plein de choses passionnantes, et je suis sûr d’en avoir manqué quelques-unes. Passez sur #i2p dans quelques minutes pour notre réunion hebdomadaire et venez dire bonjour !

=jr
