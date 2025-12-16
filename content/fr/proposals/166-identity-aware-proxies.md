---
title: "Proposition I2P #166 : Types de Tunnels Sensibles à l'Identité/Hôte"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Ouvert"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
toc: true
---

### Proposition pour un Tunnel Proxy HTTP Sensible à l'Hôte

Il s'agit d'une proposition visant à résoudre le "Problème d'Identité Partagée" dans l'utilisation conventionnelle du HTTP-sur-I2P en introduisant un nouveau type de tunnel proxy HTTP. Ce type de tunnel a un comportement supplémentaire destiné à prévenir ou limiter l'utilité du suivi effectué par des opérateurs de services cachés potentiellement hostiles, contre des agents utilisateurs ciblés (navigateurs) et l'application cliente I2P elle-même.

#### Quel est le problème de “l’Identité Partagée” ?

Le problème de “l’Identité Partagée” survient lorsqu'un agent utilisateur sur un réseau de superposition adressé de manière cryptographique partage une identité cryptographique avec un autre agent utilisateur. Cela se produit, par exemple, lorsqu'un Firefox et un GNU Wget sont tous deux configurés pour utiliser le même proxy HTTP.

Dans ce scénario, il est possible pour le serveur de collecter et stocker l'adresse cryptographique (Destination) utilisée pour répondre à l'activité. Il peut le traiter comme une “Empreinte” qui est toujours 100% unique, car elle est d'origine cryptographique. Cela signifie que la liaison observée par le problème d'Identité Partagée est parfaite.

Mais est-ce vraiment un problème ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le problème d'identité partagée est un problème lorsque des agents utilisateurs qui parlent le même protocole souhaitent une non-correlabilité. [Il a été mentionné pour la première fois dans le contexte du HTTP dans ce fil Reddit](https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/), les commentaires supprimés étant accessibles grâce à [pullpush.io](https://api.pullpush.io/reddit/search/comment/?link_id=579idi). *À l'époque*, j'étais l'un des répondants les plus actifs, et *à l'époque* je croyais que le problème était mineur. Au cours des 8 dernières années, la situation et mon opinion ont changé, je crois maintenant que la menace posée par la corrélation de destination malveillante augmente considérablement à mesure que de plus en plus de sites sont en mesure de “proﬁler” des utilisateurs spécifiques.

Cette attaque a une barrière à l'entrée très faible. Elle nécessite seulement qu'un opérateur de service caché exploite plusieurs services. Pour les attaques sur les visites contemporaines (visiter plusieurs sites en même temps), c'est la seule exigence. Pour établir un lien non-contemporain, l'un de ces services doit être un service qui héberge des “comptes” qui appartiennent à un seul utilisateur ciblé pour le suivi.

Actuellement, tout opérateur de service qui héberge des comptes utilisateurs pourra les corréler avec l'activité sur l'ensemble des sites qu'ils contrôlent en exploitant le problème d'Identité Partagée. Mastodon, Gitlab ou même des forums simples pourraient être des attaquants déguisés, tant qu'ils exploitent plus d'un service et qu'ils s'intéressent à créer un profil pour un utilisateur. Cette surveillance pourrait être menée pour le harcèlement, le gain financier, ou des raisons liées au renseignement. Actuellement, il y a des dizaines d'opérateurs majeurs qui pourraient réaliser cette attaque et en tirer des données significatives. Pour l'instant, nous leur faisons principalement confiance pour ne pas le faire, mais des acteurs qui se moquent de nos opinions pourraient facilement émerger.

Cela est directement lié à une forme assez basique de construction de profil sur le web clair où des organisations peuvent corréler des interactions sur leur site avec des interactions sur les réseaux qu'ils contrôlent. Sur I2P, car la destination cryptographique est unique, cette technique peut parfois être encore plus fiable, bien qu'elle soit privée du pouvoir supplémentaire de la géolocalisation.

L’Identité Partagée n'est pas utile contre un utilisateur qui utilise I2P uniquement pour obfuscation de géolocalisation. Elle ne peut pas non plus être utilisée pour briser l'acheminement d'I2P. C'est uniquement un problème de gestion de l'identité contextuelle.

- Il est impossible d'utiliser le problème d'Identité Partagée pour géolocaliser un utilisateur I2P.
- Il est impossible d'utiliser le problème d'Identité Partagée pour lier des sessions I2P si elles ne sont pas contemporaines.

Cependant, il est possible de l'utiliser pour dégrader l'anonymat d'un utilisateur I2P dans des circonstances qui sont probablement très courantes. Une des raisons pour lesquelles elles sont courantes est que nous encourageons l'utilisation de Firefox, un navigateur Web qui prend en charge l'opération de type “Onglet”.

- Il est *toujours* possible de produire une empreinte à partir du problème d'Identité Partagée dans *n'importe quel* navigateur Web qui prend en charge la demande de ressources tierces.
- Désactiver JavaScript n'accomplit **rien** contre le problème d'Identité Partagée.
- S'il est possible d'établir un lien entre des sessions non-contemporaines telles que par la méthode d'“empreinte” de navigateur “traditionnelle”, alors l'Identité Partagée peut être appliquée de manière transitive, ce qui permet potentiellement une stratégie de liaison non contemporaine.
- S'il est possible d'établir un lien entre une activité sur le web clair et une identité I2P, par exemple, si la cible est connectée à un site à la fois en présence I2P et en comparaison nette sur les deux côtés, l'Identité Partagée peut être appliquée de manière transitive, permettant potentiellement une dé-anonymisation complète.

Comment vous percevez la gravité du problème d'Identité Partagée tel qu'il s'applique au proxy HTTP I2P dépend d'où vous (ou plus précisément, un “utilisateur” avec peut-être des attentes non informées) pensez que l'“identité contextuelle” pour l'application réside. Il y a plusieurs possibilités :

1. HTTP est à la fois l'Application et l'Identité Contextuelle - C'est ainsi que cela fonctionne actuellement. Toutes les applications HTTP partagent une identité.
2. Le Processus est l'Application et l'Identité Contextuelle - C'est ainsi que cela fonctionne lorsqu'une application utilise une API comme SAMv3 ou I2CP, où une application crée son identité et contrôle sa durée de vie.
3. HTTP est l'Application, mais l'Hôte est l'Identité Contextuelle - C'est l'objet de cette proposition, qui traite chaque Hôte comme une potentielle “Application Web” et traite la surface de menace comme telle.

Est-ce Résoluble?
^^^^^^^^^^^^^^^^^

Il n'est probablement pas possible de créer un proxy qui répond intelligemment à chaque cas possible où son fonctionnement pourrait affaiblir l'anonymat d'une application. Cependant, il est possible de construire un proxy qui répond intelligemment à une application spécifique qui se comporte de manière prévisible. Par exemple, dans les navigateurs Web modernes, il est attendu que les utilisateurs aient plusieurs onglets ouverts, où ils interagissent avec plusieurs sites web, qui seront distingués par le nom d'hôte.

Cela nous permet d'améliorer le comportement du proxy HTTP pour ce type d'agent utilisateur HTTP en faisant correspondre le comportement du proxy à celui de l'agent utilisateur en donnant à chaque hôte sa propre Destination lorsqu'il est utilisé avec le proxy HTTP. Ce changement rend impossible l'utilisation du problème d'Identité Partagée pour dériver une empreinte qui pourrait être utilisée pour corréler l'activité du client avec deux hôtes, car les deux hôtes ne partageront simplement plus la même identité de retour.

Description :
^^^^^^^^^^^^

Un nouveau proxy HTTP sera créé et ajouté au Gestionnaire de Services Cachés (I2PTunnel). Le nouveau proxy HTTP fonctionnera comme un “multiplexeur” de I2PSocketManagers. Le multiplexeur lui-même n'a pas de destination. Chaque I2PSocketManager individuel qui devient partie du multiplex a sa propre destination locale et son propre pool de tunnels. Les I2PSocketManagers sont créés à la demande par le multiplexeur, où la “demande” est la première visite d'un nouvel hôte. Il est possible d'optimiser la création des I2PSocketManagers avant de les insérer dans le multiplexeur en en créant un ou plusieurs à l'avance et en les stockant à l'extérieur du multiplexeur. Cela peut améliorer les performances.

Un I2PSocketManager supplémentaire, avec sa propre destination, est configuré comme porteur d'un “Outproxy” pour tout site qui n'a *pas* de Destination I2P, par exemple tout site du web clair. Cela rend effectivement toute utilisation d'Outproxy une seule Identité Contextuelle, avec la mise en garde que la configuration de plusieurs Outproxies pour le tunnel entraînera la rotation normale de l'“Outproxy collant”, où chaque outproxy ne reçoit des demandes que pour un seul site. Cela est *presque* le comportement équivalent à l'isolation des proxys HTTP-sur-I2P par destination, sur l'internet clair.

Considérations de Ressources :
''''''''''''''''''''''''''''''

Le nouveau proxy HTTP nécessite des ressources supplémentaires par rapport au proxy HTTP existant. Il va :

- Construire potentiellement plus de tunnels et d'I2PSocketManagers
- Construire des tunnels plus souvent

Chacun d'eux nécessite :

- Des ressources de calcul locales
- Des ressources réseau de la part des pairs

Paramètres :
'''''''''''

Afin de minimiser l'impact de l'utilisation accrue des ressources, le proxy doit être configuré pour utiliser le moins possible. Les proxys faisant partie du multiplexeur (pas le proxy parent) doivent être configurés pour :

- Les I2PSocketManagers multiplexés construisent 1 tunnel entrant, 1 tunnel sortant dans leurs pools de tunnels
- Les I2PSocketManagers multiplexés font 3 sauts par défaut.
- Fermer les sockets après 10 minutes d'inactivité
- Les I2PSocketManagers démarrés par le Multiplexeur partagent la durée de vie du Multiplexeur. Les tunnels multiplexés ne sont pas "Détruits" jusqu'à ce que le Multiplexeur parent le soit.

Diagrammes :
^^^^^^^^^^

Le diagramme ci-dessous représente le fonctionnement actuel du proxy HTTP, qui correspond à la “Possibilité 1.” sous la section “Est-ce un problème”. Comme vous pouvez le voir, le proxy HTTP interagit avec des sites I2P directement en utilisant une seule destination. Dans ce scénario, HTTP est à la fois l'application et l'identité contextuelle.

```text
**Situation Actuelle : HTTP est l'Application, HTTP est l'Identité Contextuelle**
                                                          __-> Outproxy <-> i2pgit.org
                                                         /
   Navigateur <-> Proxy HTTP (une Destination) <-> I2PSocketManager <---> idk.i2p
                                                         \__-> translate.idk.i2p
                                                          \__-> git.idk.i2p
```

Le diagramme ci-dessous représente le fonctionnement d'un proxy HTTP sensible à l'hôte, qui correspond à la “Possibilité 3.” sous la section “Est-ce un problème”. Dans ce scénario, HTTP est l'application, mais l'Hôte définit l'identité contextuelle, où chaque site I2P interagit avec un proxy HTTP différent avec une destination unique par hôte. Cela empêche les opérateurs de plusieurs sites de pouvoir distinguer quand la même personne visite plusieurs sites qu'ils exploitent.

```text
**Après le Changement : HTTP est l'Application, l'Hôte est l'Identité Contextuelle**
                                                        __-> I2PSocketManager (Destination A - Outproxies Uniquement) <--> i2pgit.org
                                                       /
   Navigateur <-> Multiplexeur Proxy HTTP (Pas de Destination) <---> I2PSocketManager (Destination B) <--> idk.i2p
                                                       \__-> I2PSocketManager (Destination C) <--> translate.idk.i2p
                                                        \__-> I2PSocketManager (Destination C) <--> git.idk.i2p
```

Statut :
^^^^^^^

Une implémentation Java fonctionnelle du proxy sensible à l'hôte qui se conforme à une version antérieure de cette proposition est disponible sur la fourche de idk sous la branche : i2p.i2p.2.6.0-browser-proxy-post-keepalive Lien dans les citations. Elle est sous révision lourde, afin de décomposer les changements en sections plus petites.

Des implémentations avec des capacités variées ont été écrites en Go utilisant la bibliothèque SAMv3, elles peuvent être utiles pour être intégrées dans d'autres applications Go ou pour go-i2p mais ne conviennent pas pour Java I2P. De plus, elles manquent de bon support pour travailler de manière interactive avec des leaseSets cryptés.

Addendum : ``i2psocks``

Une approche simple orientée application pour isoler d'autres types de clients est possible sans mettre en œuvre un nouveau type de tunnel ou modifier le code I2P existant en combinant les outils I2PTunnel existants qui sont déjà largement disponibles et testés dans la communauté de la confidentialité. Cependant, cette approche fait une hypothèse difficile qui n'est pas vraie pour HTTP et non plus vraie pour beaucoup d'autres types de clients I2P potentiels.

En gros, le script suivant produira un proxy SOCKS5 sensible à l'application et habilitera la commande sous-jacente :

```sh
#! /bin/sh
command_to_proxy="$@"
java -jar ~/i2p/lib/i2ptunnel.jar -wait -e 'sockstunnel 7695'
torsocks --port 7695 $command_to_proxy
```

Addendum : ``exemple d'implémentation de l'attaque``

[Un exemple d'implémentation de l'attaque d'Identité Partagée sur les Agents Utilisateurs HTTP](https://github.com/eyedeekay/colluding_sites_attack/) existe depuis plusieurs années. Un exemple supplémentaire est disponible dans le sous-répertoire ``simple-colluder`` du [répertoire prop166 d’idk](https://git.idk.i2p/idk/i2p.host-aware-proxy) Ces exemples sont délibérément conçus pour démontrer que l'attaque fonctionne et nécessiteraient une modification (quoique mineure) pour être transformés en attaque réelle.

