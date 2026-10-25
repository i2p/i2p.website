---
title: "Performance"
description: "Performance du réseau I2P : vitesse, connexions et gestion des ressources"
slug: "performance"
aliases:
  - "/fr/about/performance/future"
  - "/fr/about/performance/future/"
  - "/fr/about/performance/history"
  - "/fr/about/performance/history/"
  - "/fr/performance"
  - "/fr/performance/"
  - "/fr/performance-history"
  - "/fr/performance-history/"
  - "/fr/benchmarks"
  - "/fr/benchmarks/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Performance du réseau I2P : Vitesse, connexions et gestion des ressources

Le réseau I2P est entièrement dynamique. Chaque client est connu des autres nœuds et teste localement les nœuds connus pour leur accessibilité et leur capacité. Seuls les nœuds accessibles et capables sont sauvegardés dans une netDb locale. Pendant le processus de construction de tunnel, les meilleures ressources sont sélectionnées dans ce pool pour construire des tunnels. Parce que les tests se déroulent en continu, le pool de nœuds change. Chaque nœud I2P connaît une partie différente de la netDb, ce qui signifie que chaque router dispose d'un ensemble différent de nœuds I2P à utiliser pour les tunnels. Même si deux routers ont le même sous-ensemble de nœuds connus, les tests d'accessibilité et de capacité montreront probablement des résultats différents, car les autres routers pourraient être sous charge juste au moment où un router teste, mais être libres quand le second router teste.

Ceci explique pourquoi chaque nœud I2P utilise différents nœuds pour construire des tunnels. Comme chaque nœud I2P a une latence et une bande passante différentes, les tunnels (qui sont construits via ces nœuds) ont des valeurs de latence et de bande passante différentes. Et comme chaque nœud I2P a des tunnels différents construits, aucun deux nœuds I2P n'ont les mêmes ensembles de tunnels.

Un serveur/client est appelé une "destination" et chaque destination possède au moins un tunnel entrant et un tunnel sortant. La valeur par défaut est de 3 sauts par tunnel. Cela représente un total de 12 sauts (soit 12 nœuds I2P différents) pour un aller-retour complet client-serveur-client.

Chaque paquet de données est envoyé à travers 6 autres nœuds I2P jusqu'à ce qu'il atteigne le serveur :

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
et au retour 6 nœuds I2P différents :

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
Le trafic sur le réseau nécessite un ACK avant l'envoi de nouvelles données, il doit attendre qu'un ACK revienne du serveur : envoyer des données, attendre l'ACK, envoyer plus de données, attendre l'ACK. Comme le RTT (temps d'aller-retour) s'accumule à partir de la latence de chaque nœud I2P individuel et de chaque connexion sur cet aller-retour, il faut généralement 1 à 3 secondes avant qu'un ACK revienne au client. En raison de la conception du transport TCP et I2P, un paquet de données a une taille limitée. Ensemble, ces conditions fixent une limite de bande passante maximale par tunnel de 20-50 ko/sec. Cependant, si UN SEUL saut dans le tunnel n'a que 5 ko/sec de bande passante à disposition, l'ensemble du tunnel est limité à 5 ko/sec, indépendamment de la latence et des autres limitations.

Le chiffrement, la latence et la façon dont un tunnel est construit le rendent très coûteux en temps CPU. C'est pourquoi une destination n'est autorisée à avoir qu'un maximum de 6 tunnels IN et 6 tunnels OUT pour transporter les données. Avec un maximum de 50 ko/sec par tunnel, une destination pourrait utiliser environ 300 ko/sec de trafic combiné (en réalité, cela pourrait être plus si des tunnels plus courts sont utilisés avec un anonymat faible ou inexistant). Les tunnels utilisés sont supprimés toutes les 10 minutes et de nouveaux sont construits. Ce changement de tunnels, et parfois des clients qui s'arrêtent ou perdent leur connexion au réseau, cassent parfois les tunnels et les connexions. Un exemple de ceci peut être observé sur le réseau IRC2P avec une perte de connexion (délai d'attente du ping) ou lors de l'utilisation d'eepget.

Avec un ensemble limité de destinations et un ensemble limité de tunnels par destination, un nœud I2P n'utilise qu'un ensemble limité de tunnels à travers d'autres nœuds I2P. Par exemple, si un nœud I2P est "hop1" dans le petit exemple ci-dessus, nous ne voyons qu'1 tunnel participant provenant du client. Si nous additionnons l'ensemble du réseau I2P, seul un nombre plutôt limité de tunnels participants pourrait être construit avec une quantité limitée de bande passante au total. Si l'on distribue ces nombres limités à travers le nombre de nœuds I2P, il n'y a qu'une fraction de la bande passante/capacité disponible pour utilisation.

Pour rester anonyme, un seul router ne devrait pas être utilisé par l'ensemble du réseau pour construire des tunnels. Si un router agit effectivement comme un router de tunnel pour TOUS les nœuds I2P, il devient un point de défaillance centrale très réel ainsi qu'un point central pour collecter les adresses IP et les données des clients. C'est pourquoi le réseau distribue le trafic entre les nœuds dans le processus de construction des tunnels.

Une autre considération pour les performances est la façon dont I2P gère le réseau maillé. Chaque saut de connexion utilise une connexion TCP ou UDP sur les nœuds I2P. Avec 1000 connexions, on observe 1000 connexions TCP. C'est beaucoup, et certains routeurs domestiques et de petits bureaux n'autorisent qu'un petit nombre de connexions. I2P essaie de limiter ces connexions à moins de 1500 par type UDP et par type TCP. Cela limite également la quantité de trafic acheminé à travers un nœud I2P.

Si un nœud est accessible et a un paramètre de bande passante > 128 koctets/sec partagés et est accessible 24h/24 et 7j/7, il devrait être utilisé après un certain temps pour le trafic de participation. S'il tombe en panne entre-temps, les tests d'un nœud I2P effectués par d'autres nœuds leur indiqueront qu'il n'est pas accessible. Cela bloque un nœud pendant au moins 24 heures sur d'autres nœuds. Ainsi, les autres nœuds qui ont testé ce nœud comme étant hors service n'utiliseront pas ce nœud pendant 24 heures pour construire des tunnels. C'est pourquoi votre trafic est plus faible après un redémarrage/arrêt de votre router I2P pendant un minimum de 24 heures.

De plus, les autres nœuds I2P doivent connaître un router I2P pour tester sa capacité d'accès et sa capacité. Ce processus peut être accéléré lorsque vous interagissez avec le réseau, par exemple en utilisant des applications ou en visitant des sites I2P, ce qui entraînera davantage de construction de tunnels et donc plus d'activité et de capacité d'accès pour les tests par les nœuds du réseau.

---

## Améliorations des performances

Pour de possibles améliorations de performance futures, voir [Améliorations de Performance Futures](/docs/overview/performance#future).

Pour les améliorations de performances passées, voir l'[Historique des performances](/docs/overview/performance#history).
