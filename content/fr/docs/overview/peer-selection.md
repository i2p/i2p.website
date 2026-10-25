---
title: "Profilage et sélection des pairs"
description: "Comment les routeurs I2P profilent et sélectionnent les pairs pour construire des tunnels"
slug: "peer-selection"
aliases:
  - "/fr/how_peerselection"
  - "/fr/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## Note

Cette page décrit l'implémentation Java d'I2P pour le profilage et la sélection des pairs en 2010. Bien qu'elle reste globalement exacte, certains détails peuvent ne plus être corrects. Nous continuons à faire évoluer les stratégies de bannissement, de blocage et de sélection pour faire face aux nouvelles menaces, attaques et conditions réseau. Le réseau actuel dispose de multiples implémentations de router avec diverses versions. D'autres implémentations I2P peuvent avoir des stratégies de profilage et de sélection complètement différentes, ou peuvent ne pas utiliser de profilage du tout.

## Aperçu {#overview}

### Profilage des pairs {#profiling}

**Le profilage des pairs** est le processus de collecte de données basé sur les performances **observées** d'autres routers ou pairs, et de classification de ces pairs en groupes. Le profilage n'utilise **pas** les données de performances revendiquées publiées par le pair lui-même dans la [base de données réseau](/docs/overview/network-database).

Les profils sont utilisés à deux fins :

1. Sélectionner les pairs pour relayer notre trafic, ce qui est discuté ci-dessous
2. Choisir les pairs parmi l'ensemble des routeurs floodfill à utiliser pour le stockage et les requêtes de la base de données réseau,
   ce qui est discuté sur la page [base de données réseau](/docs/overview/network-database)

### Sélection des pairs {#selection}

**La sélection de pairs** est le processus de choix des routers sur le réseau par lesquels nous voulons faire transiter nos messages (quels pairs allons-nous demander de rejoindre nos tunnels). Pour accomplir cela, nous gardons une trace de la performance de chaque pair (le "profil" du pair) et utilisons ces données pour estimer leur rapidité, la fréquence à laquelle ils seront capables d'accepter nos requêtes, et s'ils semblent surchargés ou autrement incapables d'accomplir de manière fiable ce qu'ils acceptent de faire.

Contrairement à d'autres réseaux anonymes, dans I2P, la bande passante annoncée n'est pas fiable et est **uniquement** utilisée pour éviter les pairs qui annoncent une très faible bande passante insuffisante pour le routage des tunnels. Toute sélection de pairs se fait par profilage. Cela empêche les attaques simples basées sur des pairs revendiquant une bande passante élevée afin de capturer un grand nombre de tunnels. Cela rend également les [attaques de synchronisation](/docs/overview/threat-model#timing) plus difficiles.

La sélection des pairs est effectuée très fréquemment, car un router peut maintenir un grand nombre de tunnels clients et exploratoires, et la durée de vie d'un tunnel n'est que de 10 minutes.

### Informations complémentaires {#further-info}

Pour plus d'informations, voir l'article [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) présenté à [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1). Voir [ci-dessous](#notes) pour les notes sur les changements mineurs depuis la publication de l'article.

## Profils {#profiles}

Chaque pair dispose d'un ensemble de points de données collectés à leur sujet, incluant des statistiques sur le temps qu'ils mettent à répondre à une requête de base de données réseau, la fréquence d'échec de leurs tunnels, et le nombre de nouveaux pairs qu'ils sont capables de nous présenter, ainsi que des points de données simples tels que la dernière fois que nous avons eu de leurs nouvelles ou quand la dernière erreur de communication s'est produite.

Les profils sont assez petits, quelques Ko. Pour contrôler l'utilisation de la mémoire, le temps d'expiration des profils diminue à mesure que le nombre de profils augmente. Les profils sont conservés en mémoire jusqu'à l'arrêt du router, moment où ils sont écrits sur le disque. Au démarrage, les profils sont lus afin que le router n'ait pas besoin de réinitialiser tous les profils, permettant ainsi au router de se réintégrer rapidement dans le réseau après le démarrage.

## Résumés des pairs {#summaries}

Bien que les profils eux-mêmes puissent être considérés comme un résumé des performances d'un pair, pour permettre une sélection efficace des pairs, nous décomposons chaque résumé en quatre valeurs simples, représentant la vitesse du pair, sa capacité, son degré d'intégration dans le réseau, et s'il est défaillant.

### Vitesse {#speed}

Le calcul de vitesse parcourt simplement le profil et estime la quantité de données que nous pouvons envoyer ou recevoir sur un seul tunnel à travers le pair en une minute. Pour cette estimation, il examine juste les performances de la minute précédente.

### Capacité {#capacity}

Le calcul de capacité parcourt simplement le profil et estime combien de tunnels le pair accepterait de rejoindre sur une période donnée. Pour cette estimation, il examine combien de demandes de construction de tunnel le pair a acceptées, rejetées et abandonnées, et combien des tunnels acceptés ont échoué par la suite. Bien que le calcul soit pondéré dans le temps de sorte que l'activité récente compte plus que l'activité ultérieure, des statistiques vieilles de jusqu'à 48 heures peuvent être incluses.

Reconnaître et éviter les pairs non fiables et inatteignables est d'une importance cruciale. Malheureusement, comme la construction et les tests de tunnel nécessitent la participation de plusieurs pairs, il est difficile d'identifier positivement la cause d'une demande de construction abandonnée ou d'un échec de test. Le router assigne une probabilité d'échec à chacun des pairs, et utilise cette probabilité dans le calcul de capacité. Les abandons et les échecs de tests sont pondérés beaucoup plus lourdement que les rejets.

## Organisation des pairs {#organization}

Comme mentionné ci-dessus, nous analysons en détail le profil de chaque pair pour effectuer quelques calculs clés, et sur cette base, nous organisons chaque pair en trois groupes - rapide, haute capacité et standard.

Les groupements ne sont pas mutuellement exclusifs, ni sans rapport entre eux :

- Un pair est considéré comme "haute capacité" si son calcul de capacité atteint ou
  dépasse la médiane de tous les pairs.
- Un pair est considéré comme "rapide" s'il est déjà "haute capacité" et que son
  calcul de vitesse atteint ou dépasse la médiane de tous les pairs.
- Un pair est considéré comme "standard" s'il n'est pas "haute capacité"

### Limites de Taille de Groupe {#group-limits}

La taille des groupes peut être limitée.

- Le groupe rapide est limité à 30 pairs.
  S'il y en avait plus, seuls ceux avec la note de vitesse la plus élevée sont placés dans le groupe.
- Le groupe haute capacité est limité à 75 pairs (incluant le groupe rapide).
  S'il y en avait plus, seuls ceux avec la note de capacité la plus élevée sont placés dans le groupe.
- Le groupe standard n'a pas de limite fixe, mais est quelque peu plus petit que le nombre de RouterInfos
  stockés dans la base de données réseau locale.
  Sur un router actif dans le réseau actuel, il peut y avoir environ 1000 RouterInfos et 500 profils de pairs
  (incluant ceux des groupes rapide et haute capacité).

## Recalcul et Stabilité {#recalculation}

Les résumés sont recalculés et les pairs sont retriés en groupes toutes les 45 secondes.

Les groupes tendent à être assez stables, c'est-à-dire qu'il n'y a pas beaucoup de "remaniements" dans les classements à chaque recalcul. Les pairs dans les groupes rapides et haute capacité voient plus de tunnels construits à travers eux, ce qui augmente leurs évaluations de vitesse et de capacité, ce qui renforce leur présence dans le groupe.

## Sélection des pairs {#peer-selection}

Le router sélectionne des pairs parmi les groupes ci-dessus pour construire des tunnels à travers.

### Sélection des pairs pour les tunnels clients {#client-tunnels}

Les tunnels clients sont utilisés pour le trafic d'application, comme pour les proxies HTTP et les serveurs web.

Pour réduire la susceptibilité à [certaines attaques](http://blog.torproject.org/blog/one-cell-enough) et améliorer les performances, les pairs pour construire les tunnels clients sont choisis aléatoirement dans le plus petit groupe, qui est le groupe "rapide". Il n'y a aucun biais vers la sélection de pairs qui ont été précédemment participants dans un tunnel pour le même client.

### Sélection de pairs pour les tunnels exploratoires {#exploratory-tunnels}

Les tunnels exploratoires sont utilisés à des fins administratives du router, telles que le trafic de la base de données réseau et les tests des tunnels clients. Les tunnels exploratoires sont également utilisés pour contacter des routers précédemment non connectés, c'est pourquoi ils sont appelés "exploratoires". Ces tunnels sont généralement à faible bande passante.

Les pairs pour la construction de tunnels exploratoires sont généralement choisis aléatoirement dans le groupe standard. Si le taux de succès de ces tentatives de construction est faible comparé au taux de succès de construction des tunnels clients, le router sélectionnera une moyenne pondérée de pairs aléatoirement dans le groupe haute capacité à la place. Cela aide à maintenir un taux de succès de construction satisfaisant même lorsque les performances du réseau sont médiocres. Il n'y a aucun biais vers la sélection de pairs qui étaient précédemment participants dans un tunnel exploratoire.

Comme le groupe standard inclut un sous-ensemble très large de tous les pairs que le router connaît, les tunnels exploratoires sont essentiellement construits à travers une sélection aléatoire de tous les pairs, jusqu'à ce que le taux de succès de construction devienne trop faible.

### Restrictions {#restrictions}

Pour prévenir certaines attaques simples et pour des raisons de performance, il y a les restrictions suivantes :

- Deux pairs du même espace IP /16 ne peuvent pas être dans le même tunnel.
- Un pair peut participer à un maximum de 33% de tous les tunnels créés par le router.
- Les pairs avec une bande passante extrêmement faible ne sont pas utilisés.
- Les pairs pour lesquels une tentative de connexion récente a échoué ne sont pas utilisés.

### Ordre des pairs dans les tunnels {#ordering}

Les pairs sont ordonnés dans les tunnels pour faire face à l'[attaque du prédécesseur](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([mise à jour 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)). Plus d'informations sont disponibles sur la [page des tunnels](/docs/specs/tunnel-implementation#ordering).

## Travaux futurs {#future}

- Continuer d'analyser et d'ajuster les calculs de vitesse et de capacité selon les besoins
- Implémenter une stratégie d'éjection plus agressive si nécessaire pour contrôler l'utilisation mémoire lors de la croissance du réseau
- Évaluer les limites de taille des groupes
- Utiliser les données GeoIP pour inclure ou exclure certains pairs, si configuré

## Notes {#notes}

Pour ceux qui lisent l'article [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf), veuillez garder à l'esprit les changements mineurs suivants dans I2P depuis la publication de l'article :

- Le calcul d'intégration n'est toujours pas utilisé
- Dans l'article, les "groupes" sont appelés "niveaux"
- Le niveau "Défaillant" n'est plus utilisé
- Le niveau "Non Défaillant" est maintenant nommé "Standard"

## Références {#references}

- [Profilage et sélection des pairs dans le réseau anonyme I2P](/pdf/I2P-PET-CON-2009.1.pdf)
- [Une cellule suffit](http://blog.torproject.org/blog/one-cell-enough)
- [Gardes d'entrée Tor](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Article de Murdoch 2007](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Réglages pour Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Attaques de routage à faibles ressources contre Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
