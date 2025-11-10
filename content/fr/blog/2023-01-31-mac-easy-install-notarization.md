---
title: "Mise à jour concernant la notarisation de Mac Easy Install"
date: 2023-01-31
author: "idk, sadie"
description: "L’Easy Install Bundle pour Mac est bloqué"
categories: ["release"]
API_Translate: vrai
---

Le I2P Easy-Install Bundle pour Mac connaît un blocage des mises à jour depuis les 2 dernières versions, en raison du départ de son mainteneur. Il est recommandé que les utilisateurs de l’Easy-Install Bundle pour Mac passent à l’installateur classique de style Java, qui a été récemment rétabli sur la page de téléchargement. La version 1.9.0 présente des problèmes de sécurité connus et ne convient pas à l’hébergement de services ni à un usage de longue durée. Les utilisateurs sont invités à migrer dès que possible. Les utilisateurs avancés de l’Easy-Install Bundle peuvent contourner ce problème en compilant le bundle à partir des sources et en autosignant le logiciel.

## Le processus de notarisation pour MacOS

Le processus de distribution d’une application aux utilisateurs d’Apple comporte de nombreuses étapes. Pour distribuer une application sous forme de .dmg en toute sécurité, l’application doit passer un processus de notarisation. Pour soumettre une application à la notarisation, un développeur doit signer l’application à l’aide d’un ensemble de certificats comprenant l’un destiné à la signature du code et l’autre à la signature de l’application elle-même. Cette signature doit intervenir à des étapes précises du processus de build (processus de compilation/assemblage), avant que le paquet .dmg final destiné aux utilisateurs finaux puisse être créé.

I2P Java est une application complexe et, de ce fait, le fait de faire correspondre les types de code utilisés dans l’application aux certificats d’Apple, et de déterminer où doit avoir lieu la signature afin de produire un horodatage valide, relève d’un processus d’essais et d’erreurs. C’est en raison de cette complexité que la documentation existante à l’intention des développeurs ne parvient pas à aider l’équipe à comprendre la bonne combinaison de facteurs qui aboutira à une notarisation réussie.

Ces difficultés rendent le calendrier d’achèvement de ce processus difficile à prévoir. Nous ne saurons que nous avons terminé que lorsque nous pourrons nettoyer l’environnement de build (environnement de compilation) et suivre le processus de bout en bout. La bonne nouvelle, c’est que nous sommes passés à seulement 4 erreurs lors du processus de notarisation, contre plus de 50 lors de la première tentative, et nous pouvons raisonnablement prédire que tout sera terminé avant, ou à temps pour, la prochaine version en avril.

## Options pour les nouvelles installations et mises à jour d'I2P sur macOS

Les nouveaux participants I2P peuvent toujours télécharger l’Easy Installer de la version 1.9.0 pour macOS. J’espère avoir une version prête vers la fin avril. Les mises à jour vers la dernière version seront disponibles dès que la notarisation aura été effectuée avec succès.

L’option d’installation classique est également disponible. Cela nécessitera de télécharger Java et le logiciel I2P via le programme d’installation basé sur .jar.

[Les instructions d'installation du JAR sont disponibles ici](https://geti2p.net/en/download/macos)

Les utilisateurs d'Easy-Install peuvent passer à cette dernière version en utilisant une build de développement produite localement.

[Les instructions de compilation Easy-Install sont disponibles ici](https://i2pgit.org/i2p-hackers/i2p-jpackage-mac/-/blob/master/BUILD.md)

Il est également possible de désinstaller le logiciel, de supprimer le répertoire de configuration I2P et de réinstaller I2P à l’aide du programme d’installation .jar.
