---
title: "Utiliser un IDE avec I2P"
description: "Configurer Eclipse et NetBeans pour développer I2P avec Gradle et les fichiers de projet fournis"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

<p> La branche de développement principale d'I2P (<code>i2p.i2p</code>) a été configurée pour permettre aux développeurs de mettre en place facilement deux des IDE couramment utilisés pour le développement Java : Eclipse et NetBeans. </p>

<h2>Eclipse</h2>

<p> Les branches principales de développement I2P (<code>i2p.i2p</code> et ses dérivées) contiennent <code>build.gradle</code> pour permettre une configuration facile de la branche dans Eclipse. </p>

<ol> <li> Assurez-vous d'avoir une version récente d'Eclipse. N'importe quelle version plus récente que 2017 devrait convenir. </li> <li> Clonez la branche I2P dans un répertoire (par exemple <code>$HOME/dev/i2p.i2p</code>). </li> <li> Sélectionnez « Fichier → Importer... » puis sous « Gradle » sélectionnez « Existing Gradle Project ». </li> <li> Pour « Project root directory: » choisissez le répertoire dans lequel la branche I2P a été clonée. </li> <li> Dans la boîte de dialogue « Import Options », sélectionnez « Gradle Wrapper » et appuyez sur Continuer. </li> <li> Dans la boîte de dialogue « Import Preview » vous pouvez examiner la structure du projet. Plusieurs projets devraient apparaître sous « i2p.i2p ». Appuyez sur « Terminer ». </li> <li> Terminé ! Votre espace de travail devrait maintenant contenir tous les projets de la branche I2P, et leurs dépendances de compilation devraient être correctement configurées. </li> </ol>

<h2>NetBeans</h2>

<p> Les branches principales de développement I2P (<code>i2p.i2p</code> et ses branches dérivées) contiennent des fichiers de projet NetBeans. </p>

<!-- Conserver le contenu minimal et proche de l'original ; sera mis à jour ultérieurement. -->
