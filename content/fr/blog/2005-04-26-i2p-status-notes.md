---
title: "Notes d'état d'I2P du 2005-04-26"
date: 2005-04-26
author: "jr"
description: "Brève mise à jour hebdomadaire sur la stabilité du réseau 0.5.0.7, l’avancement du transport UDP SSU avec prise en charge multi-réseaux, et le financement des primes pour tests unitaires"
categories: ["status"]
---

Salut à toutes et à tous, bref point d'état hebdomadaire aujourd'hui

* Index

1) État du réseau 2) Statut de SSU 3) Prime pour tests unitaires 4) ???

* 1) Net status

La plupart des utilisateurs sont passés assez rapidement à la version 0.5.0.7 de la semaine dernière (merci !), et le résultat global semble positif. Le réseau semble assez fiable et le bridage des tunnels antérieur a été résolu. Il reste toutefois quelques problèmes intermittents signalés par certains utilisateurs, et nous les traquons.

* 2) SSU status

La majeure partie de mon temps est consacrée au code UDP de la version 0.6, et non, ce n’est pas prêt pour une publication, et oui, il y a des progrès ;) À l’heure actuelle, il peut gérer plusieurs réseaux, en gardant certains pairs sur UDP et d’autres sur TCP avec des performances assez raisonnables. La partie difficile consiste à traiter tous les cas de congestion/contention, puisque le réseau en production sera soumis à une charge constante, mais il y a eu beaucoup de progrès à ce sujet au cours de la dernière journée environ. Plus de nouvelles quand il y aura plus de nouvelles.

* 3) Unit test bounty

Comme duck l’a mentionné sur la liste [1], zab a lancé une prime pour aider I2P avec une série de mises à jour liées aux tests - des fonds pour toute personne capable de réaliser les tâches répertoriées sur la page de la prime [2]. Nous avons reçu d’autres dons pour cette prime [3] - elle s’élève actuellement à $1000USD. Bien que ces primes n’offrent certainement pas le "tarif du marché", elles constituent un petit signe d’encouragement pour les développeurs qui souhaitent aider.

[1] http://dev.i2p.net/pipermail/i2p/2005-April/000721.html [2] http://www.i2p.net/bounty_unittests [3] http://www.i2p.net/halloffame

* 4) ???

Ok, je suis encore en retard pour la réunion... Je devrais probablement signer et envoyer ça, hein ? Passe à la réunion et on pourra aussi discuter d'autres sujets.

=jr
