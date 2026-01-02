---
title: "Rencontrez votre mainteneur : StormyCloud"
date: 2022-09-07
author: "sadie"
description: "Entretien avec les mainteneurs de l'Outproxy StormyCloud"
categories: ["general"]
API_Translate: vrai
---

## Une conversation avec StormyCloud Inc.

Avec la version [I2P Java](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release) la plus récente, l’outproxy (proxy de sortie) existant, false.i2p, a été remplacé par le nouvel outproxy StormyCloud pour les nouvelles installations d’I2P. Pour les personnes qui mettent à jour leur router, le passage au service Stormycloud peut se faire rapidement.

Dans votre Gestionnaire des services cachés, définissez Outproxies et SSL Outproxies sur exit.stormycloud.i2p, puis cliquez sur le bouton d’enregistrement en bas de la page.

## Qui est StormyCloud Inc ?

**Mission de StormyCloud Inc.**

Défendre l’accès à Internet en tant que droit humain universel. Ce faisant, le groupe protège la vie privée électronique des utilisateurs et renforce la communauté en favorisant un accès sans restriction à l’information et, par conséquent, le libre échange d’idées au-delà des frontières. C’est essentiel, car Internet est l’outil le plus puissant dont on dispose pour avoir un impact positif dans le monde.

**Énoncé de vision**

Devenir un pionnier dans la fourniture d’un Internet libre et ouvert à tous dans l’univers, car l’accès à Internet est un droit humain fondamental ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

J'ai rencontré Dustin pour lui dire bonjour et pour parler davantage de la protection de la vie privée, de la nécessité de services comme StormyCloud, et de ce qui a poussé l'entreprise à se tourner vers I2P.

**Quelle a été l'inspiration à l'origine de la création de StormyCloud ?**

Fin 2021, j’étais sur le subreddit /r/tor. Une personne avait répondu dans un fil de discussion sur la manière d’utiliser Tor en expliquant qu’elle comptait sur Tor pour rester en contact avec sa famille. Sa famille vivait aux États-Unis, mais cette personne résidait alors dans un pays où l’accès à Internet était très restreint. Elle devait être très prudente quant aux personnes avec lesquelles elle communiquait et quant à ce qu’elle disait. Pour ces raisons, elle comptait sur Tor. J’ai réfléchi au fait que je peux communiquer avec des personnes sans crainte ni restrictions et que cela devrait être le cas pour tout le monde.

L’objectif de StormyCloud est d’aider autant de personnes que possible à le faire.

**Quels ont été certains des défis rencontrés pour lancer StormyCloud ?**

Le coût — c’est absolument hors de prix. Nous avons choisi la voie du centre de données, car l’ampleur de ce que nous faisons ne permet pas de le faire sur un réseau domestique. Il y a des dépenses d’équipement et des coûts d’hébergement récurrents.

En ce qui concerne la création de l’organisation à but non lucratif, nous avons suivi la voie tracée par Emerald Onion et utilisé certains de leurs documents ainsi que les enseignements tirés de leur expérience. La communauté Tor met à disposition de nombreuses ressources très utiles.

**Quel a été l'accueil réservé à vos services ?**

En juillet, nous avons traité 1,5 milliard de requêtes DNS sur l’ensemble de nos services. Les utilisateurs apprécient qu’aucune journalisation ne soit effectuée. Les données n’existent tout simplement pas, et cela leur plaît.

**Qu'est-ce qu'un outproxy ?**

Un outproxy (proxy de sortie) est similaire aux nœuds de sortie de Tor : il permet de relayer du trafic clearnet (trafic Internet normal) à travers le réseau I2P. En d'autres termes, il permet aux utilisateurs d'I2P d'accéder à Internet en bénéficiant de la sécurité du réseau I2P.

**Qu'est-ce qui rend le StormyCloud I2P Outproxy spécial ?**

Pour commencer, nous sommes multi-homed (connectés à plusieurs réseaux), ce qui signifie que nous disposons de plusieurs serveurs qui assurent le trafic de l’outproxy. Cela garantit que le service est toujours disponible pour la communauté. Tous les journaux sur nos serveurs sont effacés toutes les 15 minutes. Cela garantit que ni les forces de l’ordre ni nous-mêmes n’ont accès à aucune donnée. Nous permettons d’accéder aux liens onion de Tor via l’outproxy, et notre outproxy est plutôt rapide.

**Comment définissez-vous la vie privée ? Quels problèmes observez-vous en matière d'empiètement et de traitement des données ?**

La confidentialité, c’est l’absence d’accès non autorisé. La transparence est importante, par exemple via l’opt‑in (consentement explicite) — comme l’illustrent les exigences du RGPD.

De grandes entreprises amassent des données qui sont utilisées pour [l’accès sans mandat aux données de localisation](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data). Les entreprises technologiques outrepassent leurs prérogatives en s’immisçant dans ce que les gens considèrent comme privé — et qui devrait l’être —, comme les photos ou les messages.

Il est important de poursuivre les efforts de sensibilisation sur la manière de protéger vos communications, et sur les outils ou applications qui aideront une personne à le faire. La façon dont nous interagissons avec l’ensemble des informations disponibles est également importante. Il faut faire confiance, mais vérifier.

**Comment I2P s'inscrit-il dans l'énoncé de mission et de vision de StormyCloud?**

I2P est un projet open source, et ce qu’il offre s’aligne sur la mission de StormyCloud Inc. I2P fournit une couche de confidentialité et de protection pour le trafic et les communications, et le projet estime que tout le monde a droit au respect de la vie privée.

Nous avons découvert I2P début 2022 en discutant avec des personnes de la communauté Tor, et nous avons aimé ce que faisait le projet. Cela nous a semblé similaire à Tor.

Lors de notre introduction à I2P et à ses fonctionnalités, nous avons constaté la nécessité d'un outproxy (proxy de sortie) fiable. Nous avons reçu un excellent soutien de la part de membres de la communauté I2P pour créer et commencer à fournir le service d'outproxy.

**Conclusion**

La nécessité d’une prise de conscience de la surveillance de ce qui devrait rester privé dans nos vies en ligne demeure constante. Toute collecte de données devrait être consentie, et la vie privée devrait aller de soi.

Lorsque nous ne pouvons pas être certains que notre trafic ou nos communications ne seront pas observés sans notre consentement, nous avons heureusement accès à des réseaux qui, par conception, anonymisent le trafic et masquent notre localisation.

Merci à StormyCloud et à toutes celles et ceux qui fournissent des outproxies (serveurs mandataires sortants) ou des nœuds pour Tor et I2P afin que les personnes puissent accéder à Internet de manière plus sûre lorsqu’elles en ont besoin. J’ai hâte de voir davantage de personnes combiner les capacités de ces réseaux complémentaires afin de créer un écosystème de protection de la vie privée plus robuste pour toutes et tous.

Pour en savoir plus sur les services de StormyCloud Inc., rendez-vous sur [https://stormycloud.org/](https://stormycloud.org/) et soutenez leur travail en faisant un don à [https://stormycloud.org/donate/](https://stormycloud.org/donate/).
