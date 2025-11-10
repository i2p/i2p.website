---
title: "Mise à jour de Jpackage pour la CVE-2022-21449 de Java"
date: 2022-04-21
author: "idk"
description: "Bundles Jpackage publiés avec des correctifs pour Java CVE-2022-21449"
categories: ["release"]
API_Translate: vrai
---

## Détails de la mise à jour

De nouveaux I2P Easy-Install bundles (paquets d’installation simplifiée) ont été générés à l’aide de la dernière version de la machine virtuelle Java, qui contient un correctif pour la CVE-2022-21449 « Psychic Signatures ». Il est recommandé aux utilisateurs des I2P Easy-Install bundles de mettre à jour dès que possible. Les utilisateurs actuels d’OSX recevront les mises à jour automatiquement, les utilisateurs de Windows doivent télécharger le programme d’installation depuis notre page de téléchargements et exécuter le programme d’installation normalement.

Le router I2P sous Linux utilise la machine virtuelle Java configurée par le système hôte. Les utilisateurs de ces plateformes devraient revenir à une version stable de Java antérieure à Java 14 afin d’atténuer la vulnérabilité jusqu’à ce que des mises à jour soient publiées par les mainteneurs des paquets. Les autres utilisateurs utilisant une JVM externe devraient mettre à jour la JVM vers une version corrigée dès que possible.
