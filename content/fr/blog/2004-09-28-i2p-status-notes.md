---
title: "Notes de statut d'I2P du 2004-09-28"
date: 2004-09-28
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P couvrant l’implémentation d’un nouveau protocole de transport, la détection automatique de l’IP et l’avancement de la version 0.4.1"
categories: ["status"]
---

Salut tout le monde, c’est l’heure de la mise à jour hebdomadaire

## Index :

1. New transport
2. 0.4.1 status
3. ???

## 1) Nouveau transport

La version 0.4.1 prend plus de temps que prévu, mais le nouveau protocole de transport et son implémentation sont en place avec tout ce qui était prévu - détection IP, établissement de connexion à faible coût, et une interface plus simple pour faciliter le débogage lorsque les connexions échouent. Cela est réalisé en abandonnant complètement l’ancien protocole de transport et en en implémentant un nouveau, même si nous conservons les mêmes mots-clés (2048bit DH + STS, AES256/CBC/PKCS#5). Si vous souhaitez examiner le protocole, il est dans la documentation. La nouvelle implémentation est également beaucoup plus propre, puisque l’ancienne version n’était qu’un ensemble de mises à jour accumulées au cours de l’année passée.

Quoi qu’il en soit, il y a quelques éléments dans le nouveau code de détection d’IP qui méritent d’être mentionnés. Le plus important, c’est que c’est entièrement facultatif - si vous indiquez une adresse IP sur la page de configuration (ou dans le router.config lui-même), elle sera toujours utilisée, quoi qu’il arrive. En revanche, si vous laissez ce champ vide, votre router laissera le premier pair qu’il contacte lui indiquer quelle est son adresse IP, sur laquelle il commencera ensuite à écouter (après l’avoir ajoutée à son propre RouterInfo et l’avoir placée dans la base de données du réseau). Eh bien, ce n’est pas tout à fait exact - si vous n’avez pas explicitement défini une adresse IP, il fera confiance à n’importe qui pour lui indiquer à quelle adresse IP il est joignable chaque fois que le pair n’a aucune connexion. Ainsi, si votre connexion Internet redémarre, en vous attribuant peut-être une nouvelle adresse DHCP, votre router fera confiance au premier pair qu’il parvient à joindre.

Oui, cela signifie qu'il n'y a plus besoin de dyndns. Vous pouvez bien sûr continuer à l'utiliser, mais ce n'est pas nécessaire.

Cependant, cela ne règle pas tout : si vous avez un NAT ou un pare-feu, connaître votre adresse IP externe n’est que la moitié du chemin : il vous faut encore ouvrir le port entrant. Mais c’est un début.

(soit dit en passant, pour les personnes qui exploitent leurs propres réseaux I2P privés ou des simulateurs, il existe une nouvelle paire de flags (indicateurs) à définir i2np.tcp.allowLocal et i2np.tcp.tagFile)

## 2) statut de la 0.4.1

Au-delà des éléments prévus sur la feuille de route pour la 0.4.1, je veux y ajouter encore quelques éléments - à la fois des correctifs de bogues et des mises à jour de la surveillance du réseau. Je suis en train de traquer des problèmes d’activité mémoire excessive en ce moment, et je veux explorer quelques hypothèses concernant les problèmes de fiabilité occasionnels sur le réseau, mais nous serons prêts à déployer la version bientôt, peut-être jeudi. Elle ne sera malheureusement pas rétrocompatible, donc la transition sera un peu cahoteuse, mais avec le nouveau processus de mise à niveau et une implémentation du transport plus tolérante, cela ne devrait pas être aussi pénible que les précédentes mises à jour non rétrocompatibles.

## 3) ???

Oui, ces deux dernières semaines, nos mises à jour ont été courtes, mais c’est parce que nous sommes sur le front, concentrés sur l’implémentation plutôt que sur différentes conceptions de haut niveau. Je pourrais vous parler des données de profilage, ou du cache de 10 000 étiquettes de connexion pour le nouveau transport, mais ce n’est pas très intéressant. Cela dit, vous avez peut-être d’autres sujets à discuter, alors passez à la réunion de ce soir et lâchez-vous.

=jr
