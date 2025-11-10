---
title: "Notes sur l'état d'I2P du 2005-06-28"
date: 2005-06-28
author: "jr"
description: "Mise à jour hebdomadaire portant sur les plans de déploiement du transport SSU, la clôture de la prime pour tests unitaires et les considérations relatives aux licences, ainsi que l’état de Kaffe Java"
categories: ["status"]
---

Salut tout le monde, c'est à nouveau l'heure de la mise à jour hebdomadaire

* Index

1) Statut de SSU 2) Statut des tests unitaires 3) Statut de Kaffe 4) ???

* 1) SSU status

Il y a eu encore quelques avancées sur le transport SSU, et je pense actuellement qu’après encore quelques tests sur le réseau en conditions réelles, nous pourrons déployer la version 0.6 sans trop de retard. La première version SSU n’inclura pas la prise en charge des personnes qui ne peuvent pas ouvrir un port dans leur pare-feu ou configurer leur NAT, mais cela sera déployé dans la 0.6.1. Une fois la 0.6.1 publiée, testée et qui déchire (alias 0.6.1.42), nous passerons à la 1.0.

Mon inclination personnelle est d’abandonner complètement le transport TCP au fur et à mesure du déploiement du transport SSU, afin que les utilisateurs n’aient pas besoin d’activer les deux (rediriger à la fois les ports TCP et UDP) et que les développeurs n’aient pas à maintenir du code inutile. Quelqu’un a-t-il un avis tranché à ce sujet ?

* 2) Unit test status

Comme mentionné la semaine dernière, Comwiz s’est manifesté pour réclamer la première phase de la prime pour les tests unitaires (youpi Comwiz ! merci aussi à duck & zab d’avoir financé la prime !). Le code a été intégré dans CVS et, selon votre configuration locale, vous pourrez peut-être générer les rapports junit et clover en allant dans le répertoire i2p/core/java et en exécutant "ant test junit.report" (attendez environ une heure...) puis consulter i2p/reports/core/html/junit/index.html. Sinon, vous pouvez exécuter "ant useclover test junit.report clover.report" et consulter i2p/reports/core/html/clover/index.html.

L'inconvénient des deux séries de tests tient à ce concept absurde que la classe dirigeante appelle "loi sur le droit d'auteur". Clover est un produit commercial, bien que les gens de chez cenqua en autorisent l'utilisation gratuite par les développeurs open source (et ils ont gentiment accepté de nous accorder une licence). Pour générer les rapports clover, vous devez avoir clover installé localement - j'ai clover.jar dans ~/.ant/lib/, à côté de mon fichier de licence. La plupart des gens n'auront pas besoin de clover, et comme nous publierons les rapports sur le web, ne pas l'installer ne fait perdre aucune fonctionnalité.

En revanche, nous nous heurtons à l’autre versant du droit d’auteur lorsque nous prenons en considération le framework de tests unitaires lui-même - junit est publié sous l’IBM Common Public License 1.0, qui, selon la FSF [1], n’est pas compatible avec la GPL. Or, même si nous n’avons pas de code GPL nous-mêmes (du moins pas dans le core ni dans le router), en nous référant à notre politique de licence [2], notre objectif, dans les détails de la manière dont nous accordons des licences, est de permettre au plus grand nombre d’utiliser ce qui est créé, car l’anonymat aime la compagnie.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

Puisque certaines personnes publient inexplicablement des logiciels sous la GPL, il est logique que nous nous efforcions de leur permettre d'utiliser I2P sans contrainte. Au minimum, cela signifie que nous ne pouvons pas autoriser que la fonctionnalité réelle que nous exposons dépende du code sous licence CPL (p. ex. junit.framework.*). J’aimerais étendre cela pour inclure également les tests unitaires, mais junit semble être la lingua franca des frameworks de test (et je ne pense pas qu’il serait ne serait-ce que vaguement sensé de dire « hey, construisons notre propre framework de test unitaire dans le domaine public ! », étant donné nos ressources).

Compte tenu de tout cela, voici ce que j'envisage. Nous inclurons junit.jar dans CVS et l'utiliserons lors de l'exécution des tests unitaires, mais les tests unitaires eux-mêmes ne seront pas intégrés dans i2p.jar ni dans router.jar, et ne seront pas inclus dans les versions publiées. Nous pourrions mettre à disposition un ensemble supplémentaire d'archives JAR (i2p-test.jar et router-test.jar), si nécessaire, mais ceux-ci ne seraient pas utilisables par des applications sous licence GPL (puisqu'ils dépendent de junit).

=jr
