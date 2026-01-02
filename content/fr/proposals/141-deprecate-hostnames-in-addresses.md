---
title: "Déprécier les noms d'hôte dans les adresses des routeurs"
number: "141"
author: "zzz"
created: "2017-08-03"
lastupdated: "2018-03-17"
status: "Fermé"
thread: "http://zzz.i2p/topics/2363"
target: "0.9.32"
implementedin: "0.9.32"
toc: true
---

## Vue d'ensemble

À partir de la version 0.9.32, mettez à jour la spécification netdb
pour déprécier les noms d'hôte dans les infos des routeurs,
ou plus précisément, dans les adresses individuelles des routeurs.
Dans toutes les implémentations I2P,
les routeurs de publication configurés avec des noms d'hôte doivent remplacer les noms d'hôte par des IP avant de publier,
et les autres routeurs doivent ignorer les adresses avec des noms d'hôte.
Les routeurs ne doivent pas effectuer de recherches DNS pour les noms d'hôte publiés.


## Motivation

Les noms d'hôte ont été autorisés dans les adresses des routeurs depuis le début d'I2P.
Cependant, très peu de routeurs publient des noms d'hôte, car cela nécessite
à la fois un nom d'hôte public (que peu d'utilisateurs possèdent) et une configuration manuelle
(que peu d'utilisateurs prennent la peine de faire).
Dans un échantillon récent, 0,7 % des routeurs publiaient un nom d’hôte.

Le but initial des noms d'hôte était d'aider les utilisateurs ayant des IP
changeantes fréquemment et un service DNS dynamique (tel que http://dyn.com/dns/)
à ne pas perdre de connectivité lorsque leur IP changeait. Cependant, à l'époque
le réseau était petit et l'expiration des infos routeur était plus longue.
De plus, le code Java n'avait pas de logique fonctionnelle pour redémarrer le routeur ou
republiquer les infos routeur lorsque l'IP locale changeait.

Aussi, au début, I2P ne supportait pas IPv6, donc la complication
de résoudre un nom d'hôte en une adresse IPv4 ou IPv6 n'existait pas.

Dans Java I2P, il a toujours été difficile de propager un nom d'hôte configuré
aux deux transports publiés, et la situation s'est compliquée
avec IPv6.
Il n'est pas clair si un hôte dual-stack doit publier à la fois un nom d'hôte et une adresse
IPv6 littérale ou non. Le nom d'hôte est publié pour l'adresse SSU mais pas pour l'adresse NTCP.

Récemment, des problèmes DNS ont été soulevés (indirectement et directement) par
des recherches à Georgia Tech. Les chercheurs ont exécuté un grand nombre de floodfills
avec des noms d'hôte publiés. Le problème immédiat était que pour un petit nombre
d'utilisateurs avec un DNS local possiblement défectueux, cela a complètement bloqué I2P.

Le problème plus large était le DNS en général, et comment
le DNS (actif ou passif) pourrait être utilisé pour énumérer très rapidement le réseau,
surtout si les routeurs de publication étaient des floodfills.
Des noms d'hôte invalides ou des répondeurs DNS non réactifs, lents ou malveillants pourraient
être utilisés pour des attaques supplémentaires.
EDNS0 peut fournir d'autres scénarios d'énumération ou d'attaque.
Le DNS peut également fournir des voies d'attaque basées sur le moment de la recherche,
révélant des temps de connexion routeur-à-routeur, aidant à construire des graphes de connexion,
à estimer le trafic, et d'autres inférences.

De plus, le groupe de Georgia Tech, dirigé par David Dagon, a listé plusieurs préoccupations
concernant le DNS dans les applications axées sur la confidentialité. Les recherches DNS sont généralement effectuées par
une bibliothèque de bas niveau, non contrôlée par l'application.
Ces bibliothèques n'ont pas été spécifiquement conçues pour l'anonymat ;
peuvent ne pas fournir un contrôle granulaire par l'application ;
et leur sortie peut être identifiée.
Les bibliothèques Java, en particulier, peuvent être problématiques, mais ce n'est pas seulement un problème Java.
Certaines bibliothèques utilisent des requêtes DNS ANY qui peuvent être rejetées.
Tout cela est rendu plus inquiétant par la présence généralisée
de la surveillance DNS passive et des requêtes disponibles pour plusieurs organisations.
Toute surveillance et attaque DNS sont hors bande du point de vue des
routeurs I2P et nécessitent peu ou pas de ressources réseau I2P,
et aucune modification des implémentations existantes.

Bien que nous n'ayons pas complètement réfléchi aux problèmes possibles,
la surface d'attaque semble être grande. Il existe d'autres moyens
d'énumérer le réseau et de collecter des données associées, mais les attaques DNS
pourraient être bien plus faciles, rapides et moins détectables.

Les implémentations de routeur pourraient, en théorie, passer à l'utilisation d'une bibliothèque
DNS 3e partie sophistiquée, mais cela serait assez complexe, représenterait une charge de maintenance
et est bien en dehors de l'expertise principale des développeurs I2P.

Les solutions immédiates mises en œuvre pour Java 0.9.31 comprenaient la correction du problème de blocage,
l'augmentation des temps de cache DNS, et l'implémentation d'un cache négatif DNS. Bien sûr,
l'augmentation des temps de cache réduit le bénéfice d'avoir des noms d'hôte dans les infos routeur au départ.

Cependant, ces changements ne sont que des atténuations à court terme et ne résolvent pas les
problèmes sous-jacents ci-dessus. Par conséquent, la solution la plus simple et la plus complète est d'interdire
les noms d'hôte dans les infos routeur, éliminant ainsi les recherches DNS pour eux.


## Conception

Pour le code de publication des infos routeur, les implémenteurs ont deux choix, soit
désactiver/enlever l'option de configuration pour les noms d'hôte, soit
convertir les noms d'hôte configurés en IPs au moment de la publication.
Dans les deux cas, les routeurs doivent republier immédiatement lorsque leur IP change.

Pour le code de validation des infos routeur et de connexion de transport,
les implémenteurs doivent ignorer les adresses de routeur contenant des noms d'hôte,
et utiliser les autres adresses publiées contenant des IPs, s'il y en a.
Si aucune adresse dans l'info routeur ne contient d'IPs, le routeur
ne doit pas se connecter au routeur publié.
En aucun cas un routeur ne doit faire une recherche DNS d'un nom d'hôte publié,
soit directement, soit via une bibliothèque sous-jacente.


## Spécification

Changer les spécifications NTCP et SSU pour indiquer que le paramètre "host" doit être
une IP, pas un nom d'hôte, et que les routeurs doivent ignorer les adresses
de routeurs individuelles qui contiennent des noms d'hôte.

Ceci s'applique également aux paramètres "ihost0", "ihost1", et "ihost2" dans une adresse SSU.
Les routeurs doivent ignorer les adresses des introducers qui contiennent des noms d'hôte.


## Notes

Cette proposition ne traite pas des noms d'hôte pour les hôtes de recensement.
Bien que les recherches DNS pour les hôtes de recensement soient beaucoup moins fréquentes,
elles pourraient encore poser un problème. Si nécessaire, cela peut être corrigé simplement
en remplaçant les noms d'hôte par des IPs dans la liste codée en dur des URLs ;
aucune modification des spécifications ou du code ne serait requise.


## Migration

Cette proposition peut être mise en œuvre immédiatement, sans migration progressive,
car très peu de routeurs publient des noms d'hôte, et ceux qui le font généralement
ne publient pas le nom d'hôte dans toutes leurs adresses.

Les routeurs n'ont pas besoin de vérifier la version du routeur publié
avant de décider d'ignorer les noms d'hôte, et il n'est pas nécessaire
d'une sortie coordonnée ou d'une stratégie commune à travers
les diverses implémentations de routeur.

Pour les routeurs qui publient encore des noms d'hôte, ils recevront moins
de connexions entrantes, et peuvent éventuellement avoir des difficultés à construire
des tunnels entrants.

Pour minimiser davantage l'impact, les implémenteurs pourraient commencer par ignorer
les adresses de routeurs avec des noms d'hôte uniquement pour les routeurs floodfill,
ou pour les routeurs avec une version publiée inférieure à 0.9.32,
et ignorer les noms d'hôte pour tous les routeurs dans une version ultérieure.
