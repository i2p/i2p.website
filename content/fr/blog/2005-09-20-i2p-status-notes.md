---
title: "Notes de statut I2P pour le 2005-09-20"
date: 2005-09-20
author: "jr"
description: "Mise à jour hebdomadaire couvrant la réussite de la version 0.6.0.6 avec les introductions SSU, la mise à jour de sécurité d’I2Phex 0.1.1.27, et l’achèvement de la migration colo (colocation)"
categories: ["status"]
---

Salut la bande, c'est encore mardi

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) migration 4) ???

* 1) 0.6.0.6

Avec la sortie 0.6.0.6 de samedi dernier, nous avons un ensemble de nouveaux éléments en place sur le réseau en production, et vous avez fait un excellent travail de mise à jour - il y a quelques heures à peine, presque 250 routers avaient effectué la mise à jour ! Le réseau semble bien se porter également, et les introductions fonctionnent jusqu’à présent - vous pouvez suivre votre propre activité d’introduction via http://localhost:7657/oldstats.jsp, en consultant udp.receiveHolePunch et udp.receiveIntroRelayResponse (ainsi que udp.receiveRelayIntro, pour ceux derrière des NAT).

Au fait, le "Status: ERR-Reject" n’est en fait plus une erreur, alors peut-être devrions-nous le changer en "Status: OK (NAT)" ?

Il y a eu quelques rapports de bug concernant Syndie. Tout récemment, il y a un bug qui fait qu’elle n’arrive pas à se synchroniser avec des pairs distants si vous lui demandez de télécharger trop d’entrées d’un coup (puisque j’ai bêtement utilisé HTTP GET au lieu de POST). Je vais ajouter la prise en charge de POST à EepGet, mais en attendant, essayez de ne récupérer que 20 ou 30 articles à la fois. Au passage, peut-être que quelqu’un peut écrire le javascript pour la page remote.jsp afin de dire « récupérer tous les articles de cet utilisateur », en cochant automatiquement toutes les cases à cocher de son blog ?

D’après les retours, OSX fonctionne correctement sans configuration particulière maintenant, et avec la version 0.6.0.6-1, x86_64 est également opérationnel sous Windows et Linux. Je n’ai pas entendu parler de problèmes avec les nouveaux installeurs .exe, donc soit tout se passe bien, soit ça échoue complètement :)

* 2) I2Phex 0.1.1.27

À la suite de certains rapports faisant état de différences entre le code source et ce qui était inclus dans le paquet de legion pour la 0.1.1.26, ainsi que d’inquiétudes quant à la sécurité du lanceur natif à code source fermé, j’ai pris l’initiative d’ajouter à cvs un nouvel i2phex.exe construit avec launch4j [1] et j’ai publié sur l’i2p file archive [2] la dernière compilation issue de cvs. On ignore s’il y a eu d’autres modifications apportées par legion à son code source avant sa publication, ou si le code source qu’il a diffusé est en fait identique à ce qu’il a compilé.

Pour des raisons de sécurité, je ne peux recommander l’utilisation ni du lanceur à code source fermé de legion, ni de la version 0.1.1.26. La version disponible sur le site web d’I2P [2] contient le dernier code issu de cvs, sans modification.

Vous pouvez reproduire le build (génération) en commençant par récupérer et compiler le code I2P, puis récupérer le code I2Phex, puis exécuter "ant makeRelease":   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (mot de passe: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

Le i2phex.exe à l’intérieur de cette archive zip est utilisable sous Windows en l’exécutant simplement, ou sous *nix/osx via "java -jar i2phex.exe". Il nécessite qu’I2Phex soit installé dans un répertoire à côté d’I2P - (par exemple C:\Program Files\i2phex\ et C:\Program Files\i2p\), car il référence certains fichiers JAR d’I2P.

Je ne prends pas en charge la maintenance d'I2Phex, mais je mettrai en ligne les futures versions d'I2Phex sur le site web lorsqu'il y aura des mises à jour de cvs. Si quelqu'un veut travailler sur une page web que nous pourrions mettre en ligne pour la décrire/la présenter (sirup, tu es là ?), avec des liens vers sirup.i2p, des messages de forum utiles, la liste des pairs actifs de legion, ce serait super.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip et     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (signé avec ma clé)

* 3) migration

Nous avons changé de serveurs en colocation pour les services I2P, mais tout devrait maintenant être pleinement opérationnel sur la nouvelle machine - si vous voyez quelque chose d’étrange, merci de me le signaler !

* 4) ???

Il y a eu pas mal de discussions intéressantes sur la liste i2p ces derniers temps, le nouveau proxy/filtre SMTP astucieux d’Adam, ainsi que quelques bons billets sur syndie (vous avez vu le thème de gloin sur http://gloinsblog.i2p ?). Je travaille en ce moment sur quelques changements concernant des problèmes de longue date, mais ils ne sont pas imminents. Si quelqu’un a autre chose à soulever et à discuter, passez à la réunion sur #i2p à 20 h GMT (dans environ 10 minutes).

=jr
