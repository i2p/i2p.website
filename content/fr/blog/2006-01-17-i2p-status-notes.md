---
title: "Notes d'état d'I2P pour le 2006-01-17"
date: 2006-01-17
author: "jr"
description: "État du réseau avec la version 0.6.1.9, améliorations cryptographiques pour la création de tunnel, et mises à jour de l'interface du blog Syndie"
categories: ["status"]
---

Salut tout le monde, on est déjà mardi

* Index

1) État du réseau et 0.6.1.9 2) Cryptographie pour la création de Tunnel 3) Blogs de Syndie 4) ???

* 1) Net status and 0.6.1.9

Avec la 0.6.1.9 publiée et 70 % du réseau mis à niveau, la plupart des correctifs inclus semblent fonctionner comme prévu; des retours indiquent que le nouveau profilage de vitesse a permis d’identifier de bons pairs. J’ai entendu parler de débits soutenus chez des pairs rapides dépassant 300KBps avec 50–70 % d’utilisation CPU, d’autres routers se situant dans la plage 100–150KBps, puis en décroissance jusqu’à ceux atteignant 1–5KBps. Il persiste toutefois une rotation importante des identités de router; il semble donc que le correctif qui, selon moi, devait réduire ce phénomène ne l’a pas fait (ou bien la rotation est légitime).

* 2) Tunnel creation crypto

À l’automne, il y a eu de nombreuses discussions sur la façon dont nous construisons nos tunnels, en parallèle des compromis entre la création de tunnels télescopiques de style Tor et la création de tunnels exploratoires de style I2P [1]. En cours de route, nous avons mis au point une combinaison [2] qui supprime les problèmes de la création de tunnels télescopiques de style Tor [3], préserve les avantages unidirectionnels d’I2P et réduit les échecs inutiles. Comme de nombreuses autres choses étaient en cours à ce moment-là, la mise en œuvre de la nouvelle combinaison a été repoussée, mais comme nous approchons désormais de la version 0.6.2, au cours de laquelle nous devons de toute façon remanier le code de création de tunnels, il est temps de finaliser cela.

J’ai rédigé une ébauche de spécification pour le nouveau chiffrement des tunnels et je l’ai publiée sur mon blog Syndie l’autre jour. Après quelques changements mineurs apparus lors de sa mise en œuvre concrète, nous avons une spécification en place dans CVS [4]. Il y a aussi du code de base qui l’implémente dans CVS [5], bien qu’il ne soit pas encore intégré à la construction effective des tunnels. Si quelqu’un s’ennuie, je serais preneur de retours sur la spécification. En attendant, je vais continuer à travailler sur le nouveau code de construction de tunnels.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html et     consultez les fils de discussion relatifs aux attaques d’amorçage [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

Comme indiqué précédemment, cette nouvelle version 0.6.1.9 comporte des refontes importantes de l’interface de blog de Syndie, notamment le nouveau style de cervantes et la sélection par chaque utilisateur des liens du blog et du logo (p. ex. [6]). Vous pouvez gérer ces liens sur la gauche en cliquant sur le lien "configurer votre blog" sur votre page de profil, ce qui vous amènera à http://localhost:7657/syndie/configblog.jsp.  Une fois que vous y aurez apporté vos modifications, la prochaine fois que vous publierez un billet dans une archive, ces informations seront mises à la disposition des autres.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Comme je suis déjà en retard de 20 minutes pour la réunion, je devrais probablement faire court. Je sais qu’il se passe quelques autres choses, mais plutôt que de les divulguer ici, les développeurs qui veulent en discuter devraient passer à la réunion et les aborder. Bref, c’est tout pour l’instant, on se retrouve sur #i2p !

=jr
