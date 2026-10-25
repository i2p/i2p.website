---
title: "Tunnels unidirectionnels"
description: "Résumé historique de la conception des tunnels unidirectionnels d'I2P"
slug: "unidirectional"
aliases:
  - "/fr/unidirectional-tunnels"
  - "/fr/unidirectional-tunnels/"
lastUpdated: "2016-11"
accurateFor: "0.9.27"
---

## Aperçu

Cette page décrit les origines et la conception des tunnels unidirectionnels d'I2P. Pour plus d'informations, voir :

- [Page de présentation des tunnels](/docs/overview/tunnel-routing)
- [Spécification des tunnels](/docs/specs/tunnel-implementation)
- [Spécification de création de tunnels](/docs/specs/tunnel-creation)
- [Discussion sur la conception des tunnels](/docs/discussions/tunnel)
- [Sélection de pairs](/docs/overview/peer-selection)

## Révision

Bien que nous ne connaissions aucune recherche publiée sur les avantages des tunnels unidirectionnels, ils semblent rendre plus difficile la détection d'un motif requête/réponse, qui est tout à fait possible à détecter sur un tunnel bidirectionnel. Plusieurs applications et protocoles, notamment HTTP, transfèrent des données de cette manière. Le fait que le trafic suive la même route vers sa destination et au retour pourrait faciliter la tâche d'un attaquant qui ne dispose que de données de timing et de volume de trafic pour déduire le chemin emprunté par un tunnel. Le fait que la réponse revienne par un chemin différent rend sans doute la tâche plus difficile.

Lorsqu'il s'agit d'un adversaire interne ou de la plupart des adversaires externes, les tunnels unidirectionnels d'I2P exposent deux fois moins de données de trafic que ce qui serait exposé avec des circuits bidirectionnels en examinant simplement les flux eux-mêmes - une requête et réponse HTTP suivraient le même chemin dans Tor, tandis que dans I2P les paquets composant la requête sortiraient par un ou plusieurs tunnels sortants et les paquets composant la réponse reviendraient par un ou plusieurs tunnels entrants différents.

La stratégie d'utilisation de deux tunnels séparés pour la communication entrante et sortante n'est pas la seule technique disponible, et elle a des implications sur l'anonymat. Du côté positif, en utilisant des tunnels séparés, cela réduit les données de trafic exposées à l'analyse pour les participants d'un tunnel - par exemple, les pairs dans un tunnel sortant depuis un navigateur web ne verraient que le trafic d'une requête HTTP GET, tandis que les pairs dans un tunnel entrant verraient la charge utile livrée le long du tunnel. Avec des tunnels bidirectionnels, tous les participants auraient accès au fait que par exemple 1KB a été envoyé dans une direction, puis 100KB dans l'autre. Du côté négatif, utiliser des tunnels unidirectionnels signifie qu'il y a deux ensembles de pairs qui doivent être profilés et pris en compte, et une attention supplémentaire doit être portée pour traiter la vitesse accrue des attaques par prédécesseur. Le processus de mise en commun et de construction des tunnels (stratégies de sélection et d'ordonnancement des pairs) devrait minimiser les préoccupations liées à l'attaque par prédécesseur.

## Anonymat

Un [article de Hermann et Grothoff](http://grothoff.org/christian/i2p.pdf) a déclaré que les tunnels unidirectionnels d'I2P "semblent être une mauvaise décision de conception".

Le point principal de l'article est que les désanonymisations sur les tunnels unidirectionnels prennent plus de temps, ce qui constitue un avantage, mais qu'un attaquant peut être plus certain dans le cas unidirectionnel. Par conséquent, l'article affirme que ce n'est pas du tout un avantage, mais un inconvénient, au moins avec les sites I2P de longue durée.

Cette conclusion n'est pas entièrement étayée par l'article. Les tunnels unidirectionnels atténuent clairement d'autres attaques et il n'est pas évident comment arbitrer le risque de l'attaque présentée dans l'article avec les attaques sur une architecture de tunnel bidirectionnel.

Cette conclusion est basée sur un arbitrage arbitraire entre certitude et temps qui peut ne pas s'appliquer dans tous les cas. Par exemple, quelqu'un pourrait établir une liste d'IP possibles puis émettre des assignations à comparaître pour chacune. Ou l'attaquant pourrait effectuer des attaques DDoS sur chacune à tour de rôle et via une simple attaque par intersection voir si le site I2P tombe en panne ou est ralenti. Donc une approximation peut suffire, ou le temps peut être plus important.

La conclusion est basée sur une pondération spécifique de l'importance de la certitude par rapport au temps, et cette pondération peut être erronée, et elle est certainement discutable, surtout dans un monde réel avec des citations à comparaître, des mandats de perquisition et d'autres méthodes disponibles pour une confirmation finale.

Une analyse complète des compromis entre les tunnels unidirectionnels et bidirectionnels dépasse clairement le cadre de cet article, et n'a pas été réalisée ailleurs. Par exemple, comment cette attaque se compare-t-elle aux nombreuses attaques de synchronisation possibles publiées sur les réseaux routés en oignon ? Il est évident que les auteurs n'ont pas effectué cette analyse, si tant est qu'il soit possible de la réaliser efficacement.

Tor utilise des tunnels bidirectionnels et a fait l'objet de nombreuses révisions académiques. I2P utilise des tunnels unidirectionnels et a fait l'objet de très peu de révisions. Le manque d'un article de recherche défendant les tunnels unidirectionnels signifie-t-il qu'il s'agit d'un mauvais choix de conception, ou simplement qu'il faut plus d'études ? Les attaques de temporisation et les attaques distribuées sont difficiles à défendre dans I2P comme dans Tor. L'intention de conception (voir les références ci-dessus) était que les tunnels unidirectionnels sont plus résistants aux attaques de temporisation. Cependant, l'article présente un type d'attaque de temporisation quelque peu différent. Cette attaque, aussi innovante soit-elle, est-elle suffisante pour qualifier l'architecture de tunnels d'I2P (et donc I2P dans son ensemble) de "mauvaise conception", et par implication clairement inférieure à Tor, ou s'agit-il simplement d'une alternative de conception qui nécessite clairement plus d'investigation et d'analyse ? Il existe plusieurs autres raisons de considérer I2P actuellement inférieur à Tor et à d'autres projets (petite taille du réseau, manque de financement, manque de révision) mais les tunnels unidirectionnels sont-ils vraiment une raison ?

En résumé, "mauvaise décision de conception" est apparemment (puisque l'article ne qualifie pas les tunnels bidirectionnels de "mauvais") un raccourci pour "les tunnels unidirectionnels sont sans équivoque inférieurs aux tunnels bidirectionnels", mais cette conclusion n'est pas soutenue par l'article.
