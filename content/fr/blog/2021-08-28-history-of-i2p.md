---
title: "20 ans de protection de la vie privée : brève histoire d'I2P"
date: 2021-08-28
slug: "20-years-of-privacy-a-brief-history-of-i2p"
author: "sadie"
description: "Un historique d'I2P tel que nous le connaissons"
categories: ["general"]
API_Translate: vrai
---

## L'invisibilité est la meilleure défense : construire un internet au sein d'Internet

> "Je crois que la plupart des gens veulent cette technologie pour pouvoir s'exprimer librement. C'est rassurant de savoir qu'on peut le faire. En même temps, nous pouvons surmonter certains des problèmes observés sur Internet en changeant la manière dont la sécurité et la vie privée sont perçues, ainsi que le degré d'importance qui leur est accordé."

En octobre 2001, 0x90 (Lance James) a eu un rêve. Cela a commencé comme un "désir de communication instantanée avec d'autres utilisateurs de Freenet pour discuter des questions liées à Freenet, et échanger des clés Freenet tout en préservant l'anonymat, la confidentialité et la sécurité." Il s'appelait IIP — the Invisible IRC Project.

The Invisible IRC Project était fondé sur un idéal et un cadre qui sous-tendaient The InvisibleNet. Dans un entretien de 2002, 0x90 décrivait le projet comme étant axé sur "l'innovation en matière de technologies de réseau intelligentes" avec pour objectif de "fournir les normes les plus élevées en matière de sécurité et de confidentialité sur un Internet largement utilisé, mais notoirement peu sécurisé."

Dès 2003, plusieurs autres projets similaires avaient vu le jour, les plus importants étant Freenet, GNUNet et Tor. Tous ces projets poursuivaient des objectifs généraux consistant à chiffrer et à anonymiser différents types de trafic. Pour IIP, il est devenu clair qu’IRC seul ne constituait pas une cible suffisamment vaste. Ce qu’il fallait, c’était une couche d’anonymisation pour tous les protocoles.

Début 2003, un nouveau développeur anonyme, "jrandom", a rejoint le projet. Son objectif explicite était d'élargir le mandat d'IIP. jrandom souhaitait réécrire la base de code d'IIP en Java et repenser les protocoles en s'appuyant sur des publications récentes et sur les premières décisions de conception que Tor et Freenet prenaient. Certains concepts, comme le "routage en oignon", ont été modifiés pour devenir le "garlic routing" (routage "garlic", concept propre à I2P).

À la fin de l’été 2003, jrandom avait pris le contrôle du projet et l’avait renommé Invisible Internet Project, ou « I2P ». Il a publié un document exposant la philosophie du projet et a replacé ses objectifs techniques et sa conception dans le contexte des mixnets (réseaux de mélange) et des couches d’anonymisation. Il a également publié les spécifications de deux protocoles (I2CP et I2NP) qui ont constitué la base du réseau qu’I2P utilise aujourd’hui.

À l’automne 2003, I2P, Freenet et Tor évoluaient rapidement. jrandom a publié I2P version 0.2 le 1er novembre 2003 et a continué à publier des versions à un rythme soutenu pendant les trois années suivantes.

En février 2005, zzz a installé I2P pour la première fois. À l'été 2005, zzz avait mis en place zzz.i2p et stats.i2p, qui sont devenus des ressources centrales pour le développement d'I2P. En juillet 2005, jrandom a publié la version 0.6, incluant le protocole de transport SSU (Secure Semi-reliable UDP) innovant pour la découverte d’adresses IP et la traversée de pare-feu.

À partir de la fin 2006 et jusque dans l’année 2007, le développement du cœur d’I2P a ralenti de façon spectaculaire, jrandom ayant déplacé son attention vers Syndie. En novembre 2007, la catastrophe a frappé lorsque jrandom a envoyé un message énigmatique indiquant qu’il devrait prendre congé pendant un an ou plus. Malheureusement, ils n’ont plus jamais eu de nouvelles de jrandom.

La deuxième étape de la catastrophe a eu lieu le 13 janvier 2008, lorsque l’entreprise d’hébergement de presque tous les serveurs i2p.net a subi une panne de courant et que le service n’a pas été entièrement rétabli. Complication, welterde et zzz ont rapidement pris des décisions pour remettre le projet en service, en migrant vers i2p2.de et en passant de CVS à monotone pour le contrôle de version.

Le projet s’est rendu compte qu’il dépendait trop fortement de ressources centralisées. Le travail mené tout au long de 2008 a décentralisé le projet et réparti les rôles entre plusieurs personnes. À partir de la version 0.7.6 du 31 juillet 2009, zzz signerait les 49 versions suivantes.

À la mi-2009, zzz avait acquis une bien meilleure compréhension de la base de code et avait identifié de nombreux problèmes de scalabilité. Le réseau a connu une croissance grâce à ses capacités d'anonymisation et de contournement. Des mises à jour automatiques via le réseau sont devenues disponibles.

À l’automne 2010, zzz a décrété un moratoire sur le développement d’I2P jusqu’à ce que la documentation du site web soit complète et exacte. Cela a pris 3 mois.

Dès 2010, zzz, ech, hottuna et d'autres contributeurs ont assisté chaque année au CCC (Chaos Communications Congress) jusqu'aux restrictions liées à la COVID-19. Le projet a fédéré la communauté et a célébré ensemble les nouvelles versions.

En 2013, Anoncoin a été créé en tant que première cryptomonnaie avec une prise en charge I2P intégrée, des développeurs comme meeh fournissant une infrastructure au réseau I2P.

En 2014, str4d a commencé à contribuer à I2PBote et, lors de Real World Crypto, des discussions ont été entamées sur la mise à jour de la cryptographie d’I2P. À la fin de 2014, la plupart des nouvelles primitives de signature étaient finalisées, notamment ECDSA et EdDSA.

En 2015, I2PCon a eu lieu à Toronto, avec des conférences, le soutien de la communauté et des participants venant d'Amérique et d'Europe. En 2016, lors de Real World Crypto à Stanford, str4d a fait une présentation sur l'avancement de la migration cryptographique.

NTCP2 a été implémenté en 2018 (version 0.9.36), offrant une résistance à la censure par inspection approfondie des paquets (DPI) et réduisant la charge du processeur grâce à une cryptographie plus rapide et moderne.

En 2019, l'équipe a participé à davantage de conférences, notamment DefCon et Monero Village, afin d'entrer en contact avec des développeurs et des chercheurs. Les travaux de Hoàng Nguyên Phong sur la censure d'I2P ont été acceptés à FOCI à USENIX, ce qui a conduit à la création d'I2P Metrics.

Lors du CCC 2019, la décision a été prise de migrer de Monotone vers GitLab. Le 10 décembre 2020, le projet est officiellement passé de Monotone à Git, rejoignant le monde des développeurs utilisant Git.

0.9.49 (2021) a commencé la migration vers un nouveau chiffrement ECIES-X25519 plus rapide pour les routers, achevant des années de travail de spécification. La migration devait s’étaler sur plusieurs versions.

## 1.5.0 — La version anniversaire anticipée

Après 9 ans de versions 0.9.x, le projet est passé directement de la version 0.9.50 à la version 1.5.0 en reconnaissance de près de 20 ans de travail pour offrir l’anonymat et la sécurité. Cette version a achevé la mise en œuvre de messages de construction de tunnel plus petits afin de réduire la consommation de bande passante et a poursuivi la transition vers le chiffrement X25519.

**Félicitations à l'équipe. Faisons-en 20 de plus.**
