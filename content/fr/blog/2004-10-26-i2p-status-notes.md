---
title: "Notes d'état d'I2P pour le 2004-10-26"
date: 2004-10-26
author: "jr"
description: "Mise à jour hebdomadaire du statut d'I2P couvrant la stabilité du réseau, le développement de la bibliothèque de streaming, les progrès de mail.i2p et les avancées de BitTorrent"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour hebdomadaire

## Index

1. Net status
2. Streaming lib
3. mail.i2p progress
4. ???

## 1) État du réseau

Je ne veux pas tenter le diable, mais depuis une semaine le réseau est à peu près comme avant - assez stable pour l'irc, les eepsites(I2P Sites) se chargent de façon fiable, même si les gros fichiers nécessitent encore souvent une reprise du téléchargement. En gros, rien de nouveau à signaler, si ce n'est qu'il n'y a rien de nouveau à signaler.

Ah, une chose que nous avons constatée, c’est que bien que Jetty prenne en charge la reprise HTTP, il ne le fait que pour HTTP 1.1. Cela convient à la plupart des navigateurs et des outils de téléchargement, *sauf* wget - wget envoie la requête de reprise en HTTP 1.0. Donc, pour télécharger de gros fichiers, utilisez curl ou un autre outil compatible avec la reprise HTTP 1.1 (merci à duck et ardvark d’avoir creusé et trouvé une solution !)

## 2) Bibliothèque de streaming

Comme le réseau a été assez stable, j'ai consacré presque tout mon temps à travailler sur la nouvelle bibliothèque de streaming. Bien qu'elle ne soit pas encore terminée, il y a eu beaucoup de progrès : les scénarios de base fonctionnent tous correctement, les fenêtres glissantes fonctionnent bien pour l'autocadencement, et la nouvelle bibliothèque fonctionne comme un remplacement "drop-in" (sans modification du code) de l'ancienne, du point de vue du client (les deux bibliothèques de streaming ne peuvent pas communiquer entre elles toutefois).

The last few days I've been working through some more interesting scenarios. The most important one is the laggy network, which we simulate by injecting delays on messages received - either a simple 0-30s random delay or a tiered delay (80% of the time have a 0-10s lag, 10% @ 10-20s lag, 5% @ 20-30s, 3% @ 30-40s, 4% @ 40-50s). Another important test has been the random dropping of messages - this shouldn't be common on I2P, but we should be able to deal with it.

Les performances globales ont été plutôt bonnes, mais il reste encore beaucoup de travail avant que nous puissions déployer cela sur le réseau en production. Cette mise à jour sera 'dangereuse' dans la mesure où elle est extrêmement puissante - si c'est fait de manière catastrophique, nous pouvons nous infliger un DDoS en un instant, mais si c'est bien fait, eh bien, disons simplement qu'il y a énormément de potentiel (annoncer peu et livrer beaucoup).

Cela dit, et puisque le réseau est plutôt « en régime stable », je ne suis pas pressé de déployer quelque chose qui n'est pas suffisamment testé. Plus de nouvelles quand il y en aura.

## 3) avancement de mail.i2p

postman et son équipe ont beaucoup travaillé sur la messagerie via I2P (voir www.postman.i2p), et des nouveautés enthousiasmantes sont en préparation - peut-être postman a-t-il une mise à jour pour nous ?

Soit dit en passant, je comprends et partage les demandes pour une interface webmail, mais postman est débordé, car il travaille sur des fonctionnalités intéressantes au niveau du back-end du système de messagerie. Une alternative, toutefois, consiste à installer une interface webmail *localement* sur votre propre serveur web - il existe des solutions webmail en JSP/servlet. Cela vous permettrait d’exécuter votre propre interface webmail locale, par exemple à l’adresse `http://localhost:7657/mail/`

Je sais qu’il existe des scripts open source pour accéder à des comptes POP3, ce qui nous amène déjà à mi-chemin - peut-être que quelqu’un pourrait en chercher qui prennent en charge POP3 et le SMTP authentifié ? Allez, vous savez que ça vous tente !

## 4) ???

Ok, c’est tout ce que j’ai à dire pour l’instant - passe à la réunion dans quelques minutes et dis-nous ce qui se passe.

=jr
