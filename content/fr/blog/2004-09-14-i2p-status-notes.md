---
title: "Notes d'état I2P du 2004-09-14"
date: 2004-09-14
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P couvrant la publication de la version 0.4.0.1, les mises à jour du modèle de menace, les améliorations du site web, les modifications de la feuille de route et les besoins en développement d’applications clientes"
categories: ["status"]
---

Salut tout le monde, c'est encore ce moment de la semaine

## Index :

1. 0.4.0.1
2. Threat model updates
3. Website updates
4. Roadmap
5. Client apps
6. ???

## 1) 0.4.0.1

Depuis la sortie de la version 0.4.0.1 mercredi dernier, les choses se passent plutôt bien sur le réseau - plus des deux tiers du réseau ont été mis à niveau, et nous maintenons entre 60 et 80 routers sur le réseau. Les durées de connexion IRC varient, mais dernièrement des connexions de 4 à 12 heures sont devenues la norme. Il y a toutefois eu quelques signalements de dysfonctionnements au démarrage sur OS/X, mais je crois que des progrès sont également réalisés sur ce front.

## 2) Mises à jour du modèle de menace

Comme mentionné en réponse au message de Toni, il y a eu une refonte assez substantielle du modèle de menace. La principale différence est que, plutôt que d’aborder les menaces de manière ad hoc comme auparavant, j’ai essayé de suivre certaines des taxonomies proposées dans la littérature. Le plus gros problème pour moi a été de trouver comment faire entrer les techniques concrètes que les gens peuvent utiliser dans les cadres proposés — souvent une seule attaque entrait dans plusieurs catégories différentes. Par conséquent, je ne suis pas vraiment satisfait de la manière dont les informations de cette page sont présentées, mais c’est mieux qu’avant.

## 3) Mises à jour du site web

Grâce à l’aide de Curiosity, nous avons commencé des mises à jour du site web - dont la plus visible apparaît sur la page d’accueil elle-même. Cela devrait aider les personnes qui tombent sur I2P par hasard et veulent savoir d’emblée ce que c’est que ce foutu I2P, plutôt que d’avoir à chercher à tâtons parmi les différentes pages. Quoi qu’il en soit, progrès, toujours en avant :)

## 4) Feuille de route

À propos des progrès, j’ai enfin mis sur pied une feuille de route remaniée, basée sur ce que, selon moi, nous devons implémenter et sur ce qui doit être accompli pour répondre aux besoins de l’utilisateur. Les principaux changements apportés à l’ancienne feuille de route sont :

- Drop AMOC altogether, replaced with UDP (however, we'll support TCP for those who can't use UDP *cough*mihi*cough*)
- Kept all of the restricted route operation to the 2.0 release, rather than bring in partial restricted routes earlier. I believe we'll be able to meet the needs of many users without restricted routes, though of course with them many more users will be able to join us. Walk before run, as they say.
- Pulled the streaming lib in to the 0.4.3 release, as we don't want to go 1.0 with the ~4KBps per stream limit. The bounty on this is still of course valid, but if no one claims it before 0.4.2 is done, I'll start working on it.
- TCP revamp moved to 0.4.1 to address some of our uglier issues (high CPU usage when connecting to people, the whole mess with "target changed identities", adding autodetection of IP address)

Les autres éléments prévus pour diverses versions 0.4.* ont déjà été implémentés. Cependant, il y a un autre élément retiré de la feuille de route...

## 5) Applications clientes

Nous avons besoin d’applications clientes. Des applications qui soient attrayantes, sécurisées, évolutives et anonymes. I2P en soi ne fait pas grand-chose, il permet simplement à deux points de terminaison de communiquer anonymement. Même si I2PTunnel offre un sacré couteau suisse, ce genre d’outil n’est vraiment attrayant que pour les geeks parmi nous. Nous avons besoin de plus que cela - nous avons besoin de quelque chose qui permette aux gens de faire ce qu’ils veulent réellement faire, et qui les aide à le faire mieux. Nous avons besoin d’une raison pour que les gens utilisent I2P au-delà du simple fait qu’il est plus sûr.

Jusqu’ici, j’ai mis en avant MyI2P pour répondre à ce besoin — un système de blog distribué offrant une interface de type LiveJournal. J’ai récemment discuté sur la liste de certaines des fonctionnalités de MyI2P. Cependant, je l’ai retiré de la feuille de route, car cela représente tout simplement trop de travail pour moi si je veux encore pouvoir accorder au réseau I2P de base l’attention dont il a besoin (notre planning est déjà extrêmement serré).

Il y a quelques autres applications qui ont beaucoup de potentiel. Stasher fournirait une infrastructure importante pour le stockage de données distribué, mais je ne sais pas vraiment où cela en est. Même avec Stasher, toutefois, il faudrait une interface utilisateur attrayante (bien que certaines applications FCP puissent fonctionner avec Stasher).

L’IRC est également un système puissant, bien qu’il présente des limites dues à son architecture basée sur des serveurs. oOo a toutefois travaillé à la mise en œuvre d’un DCC (connexion directe entre clients) transparent, de sorte que la partie IRC pourrait être utilisée pour la discussion publique et le DCC pour des transferts de fichiers privés ou une discussion sans serveur.

La fonctionnalité générale des eepsite(I2P Site) est également importante, et ce dont nous disposons actuellement est complètement insatisfaisant. Comme le souligne DrWoo, la configuration actuelle comporte des risques importants pour l’anonymat, et même si oOo a réalisé quelques correctifs filtrant certains en-têtes, il reste encore beaucoup de travail avant que les eepsites(I2P Sites) puissent être considérés comme sécurisés. Il existe plusieurs approches pour y remédier, toutes susceptibles de fonctionner, mais qui exigent toutes du travail. Je sais toutefois que duck a mentionné qu’il avait quelqu’un qui travaillait sur quelque chose, mais j’ignore où ça en est ni si cela pourrait être intégré à I2P pour que tout le monde puisse l’utiliser ou non. Duck ?

Une autre paire d’applications clientes susceptibles d’aider serait soit une application de transfert de fichiers en essaim (à la BitTorrent), soit une application de partage de fichiers plus traditionnelle (à la DC/Napster/Gnutella/etc). C’est, je pense, ce que souhaite un grand nombre de personnes, mais chacun de ces systèmes pose des problèmes. Cependant, ils sont bien connus et le portage ne poserait peut-être pas trop de difficultés (peut-être).

D’accord, donc ce qui précède n’a rien de nouveau — pourquoi ai-je tout mentionné ? Eh bien, nous devons trouver un moyen de mettre en œuvre une application cliente attrayante, sécurisée, évolutive et anonyme, et cela ne va pas se faire tout seul, comme par magie. J’ai fini par accepter que je ne pourrai pas le faire moi-même, donc nous devons être proactifs et trouver un moyen d’y parvenir.

Pour ce faire, je pense que notre système de primes pourrait aider, mais je crois que si nous n’avons pas vu beaucoup d’activité à ce sujet (des personnes se mettant à travailler pour décrocher une prime), c’est parce qu’ils sont trop dispersés. Pour obtenir les résultats dont nous avons besoin, je pense qu’il faut hiérarchiser ce que nous voulons et concentrer nos efforts sur l’élément prioritaire, en augmentant la prime afin, espérons-le, d’encourager quelqu’un à se manifester et à travailler sur la prime.

Mon avis personnel reste qu’un système de blog sécurisé et distribué comme MyI2P serait la meilleure option. Plutôt que de simplement transférer des données anonymement dans un sens et dans l’autre, il offre un moyen de construire des communautés, le cœur de tout effort de développement. De plus, il offre un rapport signal/bruit relativement élevé, un faible risque d’abus des ressources communes et, de manière générale, une faible charge sur le réseau. En revanche, il n’offre pas toute la richesse des sites Web classiques, mais les 1,8 million d’utilisateurs actifs de LiveJournal ne semblent pas s’en soucier.

Au-delà de cela, assurer la sécurité de l’architecture eepsite(I2P Site) serait ma préférence suivante, offrant aux navigateurs la sécurité dont ils ont besoin et permettant aux utilisateurs de servir des eepsites(I2P Sites) 'prêt à l'emploi'.

Le transfert de fichiers et le stockage distribué de données sont également incroyablement puissants, mais ils ne semblent pas être aussi orientés vers la communauté que nous le voudrions probablement pour la première application destinée aux utilisateurs finaux.

Je veux que toutes les applications répertoriées soient implémentées dès hier, ainsi qu’un millier d’autres applications que je n’oserais même pas imaginer. Je veux aussi la paix dans le monde, la fin de la faim, la destruction du capitalisme, l’éradication du statisme, du racisme, du sexisme et de l’homophobie, la fin de la destruction pure et simple de l’environnement et toutes ces autres choses néfastes. Cependant, nous ne sommes pas si nombreux et nous ne pouvons accomplir qu’un certain nombre de choses. Par conséquent, nous devons établir des priorités et concentrer nos efforts sur ce que nous pouvons réaliser, plutôt que de rester là, paralysés par l’ampleur de tout ce que nous voudrions faire.

Peut-être pourrions-nous discuter de quelques idées sur ce que nous devrions faire lors de la réunion de ce soir.

## 6) ???

Eh bien, c’est tout ce que j’ai pour le moment, et hé, j’ai rédigé les notes de statut *avant* la réunion ! Alors pas d’excuses, passez à 21 h GMT et bombardez-nous tous de vos idées.

=jr
