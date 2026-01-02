---
title: "Performance"
description: "Performance du réseau I2P : son comportement actuel, les améliorations historiques et les pistes d'optimisation futures"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Performance du réseau I2P : Vitesse, connexions et gestion des ressources

Le réseau I2P est entièrement dynamique. Chaque client est connu des autres nœuds et teste localement les nœuds connus pour vérifier leur accessibilité et leur capacité. Seuls les nœuds accessibles et capables sont enregistrés dans une NetDB locale. Pendant le processus de construction de tunnel, les meilleures ressources sont sélectionnées dans ce pool pour construire les tunnels. Comme les tests se déroulent en continu, le pool de nœuds évolue. Chaque nœud I2P connaît une partie différente de la NetDB, ce qui signifie que chaque routeur dispose d'un ensemble différent de nœuds I2P à utiliser pour les tunnels. Même si deux routeurs ont le même sous-ensemble de nœuds connus, les tests d'accessibilité et de capacité donneront probablement des résultats différents, car les autres routeurs pourraient être sous charge au moment où un routeur effectue ses tests, mais être disponibles lorsque le second routeur effectue les siens.

Ceci explique pourquoi chaque nœud I2P dispose de nœuds différents pour construire des tunnels. Parce que chaque nœud I2P a une latence et une bande passante différentes, les tunnels (qui sont construits via ces nœuds) ont des valeurs de latence et de bande passante différentes. Et parce que chaque nœud I2P a des tunnels construits différemment, aucun deux nœuds I2P n'a les mêmes ensembles de tunnels.

Un serveur/client est appelé une "destination" et chaque destination possède au moins un tunnel entrant et un tunnel sortant. La valeur par défaut est de 3 sauts par tunnel. Cela représente un total de 12 sauts (12 nœuds I2P différents) pour un aller-retour complet client → serveur → client.

Chaque paquet de données est envoyé à travers 6 autres nœuds I2P jusqu'à ce qu'il atteigne le serveur :

client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - serveur

et au retour 6 nœuds I2P différents :

server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client

Le trafic sur le réseau nécessite un ACK avant l'envoi de nouvelles données ; il doit attendre qu'un ACK revienne du serveur : envoyer des données, attendre l'ACK, envoyer plus de données, attendre l'ACK. Comme le RTT (Round Trip Time) s'accumule à partir de la latence de chaque nœud I2P individuel et de chaque connexion sur cet aller-retour, il faut généralement 1 à 3 secondes avant qu'un ACK revienne au client. En raison de la conception du transport TCP et I2P, un paquet de données a une taille limitée. Ensemble, ces conditions fixent une limite de bande passante maximale par tunnel d'environ 20 à 50 ko/s. Cependant, si un seul hop dans le tunnel ne dispose que de 5 ko/s de bande passante, l'ensemble du tunnel est limité à 5 ko/s, indépendamment de la latence et des autres limitations.

Le chiffrement, la latence et la façon dont un tunnel est construit le rendent assez coûteux en temps CPU. C'est pourquoi une destination n'est autorisée à avoir qu'un maximum de 6 tunnels entrants et 6 tunnels sortants pour transporter des données. Avec un maximum de 50 kB/s par tunnel, une destination pourrait utiliser environ 300 kB/s de trafic combiné (en réalité cela pourrait être plus si des tunnels plus courts sont utilisés avec une anonymat faible ou inexistant). Les tunnels utilisés sont éliminés toutes les 10 minutes et de nouveaux sont construits. Ce changement de tunnels, et parfois des clients qui s'arrêtent ou perdent leur connexion au réseau, va parfois casser des tunnels et des connexions. Un exemple de cela peut être observé sur le réseau IRC2P par une perte de connexion (ping timeout) ou lors de l'utilisation d'eepget.

Avec un ensemble limité de destinations et un ensemble limité de tunnels par destination, un nœud I2P n'utilise qu'un ensemble limité de tunnels à travers d'autres nœuds I2P. Par exemple, si un nœud I2P est "hop1" dans le petit exemple ci-dessus, il ne voit qu'un seul tunnel participant provenant du client. Si nous additionnons l'ensemble du réseau I2P, seul un nombre relativement limité de tunnels participants pourrait être construit avec une quantité limitée de bande passante au total. Si l'on répartit ces nombres limités sur le nombre de nœuds I2P, il n'y a qu'une fraction de la bande passante/capacité disponible utilisable.

Pour rester anonyme, un seul routeur ne devrait pas être utilisé par l'ensemble du réseau pour construire des tunnels. Si un routeur agit comme routeur de tunnel pour tous les nœuds I2P, il devient un point de défaillance central très réel ainsi qu'un point central pour collecter les adresses IP et les données des clients. C'est pourquoi le réseau distribue le trafic entre les nœuds dans le processus de construction de tunnels.

Un autre aspect à considérer pour les performances est la manière dont I2P gère le réseau maillé. Chaque saut de connexion hop-to-hop utilise une connexion TCP ou UDP sur les nœuds I2P. Avec 1000 connexions, on observe 1000 connexions TCP. C'est énorme, et certains routeurs domestiques et de petits bureaux n'autorisent qu'un petit nombre de connexions. I2P tente de limiter ces connexions à moins de 1500 par type UDP et par type TCP. Cela limite également la quantité de trafic acheminé à travers un nœud I2P.

Si un nœud est joignable, dispose d'un paramètre de bande passante partagée supérieur à 128 ko/s et est accessible 24h/24 et 7j/7, il devrait être utilisé après un certain temps pour le trafic participant. S'il est indisponible entre-temps, les tests d'un nœud I2P effectués par d'autres nœuds leur indiqueront qu'il n'est pas joignable. Cela bloque un nœud pendant au moins 24 heures sur les autres nœuds. Ainsi, les autres nœuds qui ont testé ce nœud comme étant indisponible ne l'utiliseront pas pendant 24 heures pour la construction de tunnels. C'est pourquoi votre trafic est plus faible après un redémarrage/arrêt de votre routeur I2P pendant un minimum de 24 heures.

De plus, les autres nœuds I2P doivent connaître un routeur I2P pour tester sa joignabilité et sa capacité. Ce processus peut être accéléré lorsque vous interagissez avec le réseau, par exemple en utilisant des applications ou en visitant des sites I2P, ce qui entraînera davantage de construction de tunnels et donc plus d'activité et de joignabilité pour les tests effectués par les nœuds du réseau.

## Historique des performances (sélection)

Au fil des années, I2P a connu un certain nombre d'améliorations de performance notables :

### Native math

Implémenté via des liaisons JNI vers la bibliothèque GNU MP (GMP) pour accélérer `modPow` de BigInteger, qui dominait auparavant le temps CPU. Les premiers résultats ont montré des accélérations spectaculaires en cryptographie à clé publique. Voir : /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Auparavant, les réponses nécessitaient souvent une recherche dans la base de données réseau pour le LeaseSet de l'expéditeur. L'inclusion du LeaseSet de l'expéditeur dans le garlic initial améliore la latence des réponses. Cela se fait désormais de manière sélective (au début d'une connexion ou lorsque le LeaseSet change) afin de réduire la surcharge.

### Mathématiques natives

Déplacé certaines étapes de validation plus tôt dans la poignée de main du transport pour rejeter les pairs défectueux plus rapidement (horloges incorrectes, mauvais NAT/pare-feu, versions incompatibles), économisant ainsi du CPU et de la bande passante.

### Envelopper en garlic un LeaseSet de "réponse" (ajusté)

Utilisez des tests de tunnels sensibles au contexte : évitez de tester les tunnels dont on sait déjà qu'ils transmettent des données ; privilégiez les tests en période d'inactivité. Cela réduit la charge et accélère la détection des tunnels défaillants.

### Rejet TCP plus efficace

La persistance des sélections pour une connexion donnée réduit la livraison hors séquence et permet à la bibliothèque de streaming d'augmenter la taille des fenêtres, améliorant ainsi le débit.

### Ajustements des tests de tunnel

GZip ou similaire pour les structures volumineuses (par exemple, options RouterInfo) réduit la bande passante lorsque approprié.

### Sélection persistante de tunnel/lease

Remplacement du protocole simpliste « ministreaming ». Le streaming moderne inclut des ACK sélectifs et un contrôle de congestion adapté au substrat anonyme et orienté messages d'I2P. Voir : /docs/api/streaming/

## Future Performance Improvements (historical ideas)

Ci-dessous se trouvent des idées documentées historiquement comme des améliorations potentielles. Beaucoup sont obsolètes, implémentées, ou remplacées par des changements architecturaux.

### Compresser les structures de données sélectionnées

Améliorer la façon dont les routeurs choisissent les pairs pour la construction de tunnels afin d'éviter ceux qui sont lents ou surchargés, tout en restant résistant aux attaques Sybil par des adversaires puissants.

### Protocole de streaming complet

Réduire l'exploration inutile lorsque l'espace de clés est stable ; ajuster le nombre de pairs renvoyés dans les recherches et le nombre de recherches concurrentes effectuées.

### Session Tag tuning and improvements (legacy)

Pour le schéma hérité ElGamal/AES+SessionTag, des stratégies d'expiration et de réapprovisionnement plus intelligentes réduisent les replis sur ElGamal et les balises gaspillées.

### Meilleur profilage et sélection des pairs

Générer des tags à partir d'un PRNG synchronisé initialisé lors de l'établissement d'une nouvelle session, réduisant ainsi la charge par message liée aux tags pré‑distribués.

### Optimisation de la base de données réseau

Des durées de vie de tunnel plus longues couplées à la réparation peuvent réduire les coûts de reconstruction ; à équilibrer avec l'anonymat et la fiabilité.

### Ajustement et améliorations des Session Tags (legacy)

Rejeter les pairs invalides plus tôt et rendre les tests de tunnel plus sensibles au contexte pour réduire la contention et la latence.

### Migrer SessionTag vers un PRNG synchronisé (ancien)

Le bundling sélectif de LeaseSet, les options de RouterInfo compressé, et l'adoption du protocole de streaming complet contribuent tous à une meilleure performance perçue.

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

Voir aussi :

- [Routage de tunnel](/docs/overview/tunnel-routing/)
- [Sélection des pairs](/docs/overview/tunnel-routing/)
- [Transports](/docs/overview/transport/)
- [Spécification SSU2](/docs/specs/ssu2/) et [Spécification NTCP2](/docs/specs/ntcp2/)
