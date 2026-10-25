---
title: "Modèle de menaces d'I2P"
description: "Analyse des attaques considérées dans la conception d'I2P et des mesures d'atténuation en place"
slug: "threat-model"
aliases:
  - "/fr/how_threatmodel"
  - "/fr/how_threatmodel/"
lastUpdated: "2010-11"
accurateFor: "0.8.1"
---

## Que voulons-nous dire par « Anonyme » ?

Votre niveau d'anonymat peut être décrit comme "la difficulté pour quelqu'un de découvrir des informations que vous ne voulez pas qu'il connaisse" — qui vous êtes, où vous vous trouvez, avec qui vous communiquez, ou même quand vous communiquez. L'anonymat "parfait" n'est pas un concept utile ici — un logiciel ne vous rendra pas indiscernable de personnes qui n'utilisent pas d'ordinateurs ou qui ne sont pas sur Internet. Au lieu de cela, nous travaillons pour fournir un anonymat suffisant pour répondre aux besoins réels de tous ceux que nous pouvons aider — de ceux qui naviguent simplement sur des sites web, à ceux qui échangent des données, jusqu'à ceux qui craignent d'être découverts par des organisations ou des États puissants.

La question de savoir si I2P fournit un anonymat suffisant pour vos besoins particuliers est difficile, mais cette page espère vous aider à répondre à cette question en explorant comment I2P fonctionne sous diverses attaques afin que vous puissiez décider s'il répond à vos besoins.

Nous encourageons la poursuite de la recherche et de l'analyse sur la résistance d'I2P aux menaces décrites ci-dessous. Une revue plus approfondie de la littérature existante (dont une grande partie se concentre sur Tor) et des travaux originaux axés sur I2P sont nécessaires.

---

## Résumé de la topologie réseau

I2P s'appuie sur les idées de nombreux [autres](/docs/overview/comparison/) systèmes, mais quelques points clés doivent être gardés à l'esprit lors de l'examen de la littérature connexe :

- **I2P est un mixnet de routage libre** — le créateur du message définit explicitement le chemin par lequel les messages seront envoyés (le tunnel sortant), et le destinataire du message définit explicitement le chemin par lequel les messages seront reçus (le tunnel entrant).
- **I2P n'a pas de points d'entrée et de sortie officiels** — tous les pairs participent pleinement au mélange, et il n'y a pas de proxies d'entrée ou de sortie au niveau de la couche réseau (cependant, au niveau de la couche application, quelques proxies existent).
- **I2P est entièrement distribué** — il n'y a pas de contrôles centraux ou d'autorités. On pourrait modifier certains routers pour faire fonctionner des cascades de mélange (construisant des tunnels et distribuant les clés nécessaires pour contrôler le transfert au point de terminaison du tunnel) ou un profilage et une sélection basés sur un répertoire, tout cela sans rompre la compatibilité avec le reste du réseau, mais le faire n'est bien sûr pas nécessaire (et peut même nuire à son anonymat).

Nous avons documenté des plans pour implémenter des délais non triviaux et des stratégies de traitement par lots dont l'existence n'est connue que du saut particulier ou de la passerelle tunnel qui reçoit le message, permettant à un mixnet principalement à faible latence de fournir du trafic de couverture pour les communications à latence plus élevée (par ex. email). Cependant, nous sommes conscients que des délais significatifs sont nécessaires pour fournir une protection significative, et que l'implémentation de tels délais constituera un défi considérable. Il n'est pas clair à ce moment si nous implémenterons réellement ces fonctionnalités de délai.

En théorie, les routers le long du chemin du message peuvent injecter un nombre arbitraire de sauts avant de transmettre le message au pair suivant, bien que l'implémentation actuelle ne le fasse pas.

---

## Le modèle de menace

La conception d'I2P a commencé en 2003, peu de temps après l'avènement du [Onion Routing](http://www.onion-router.net), de [Freenet](http://freenetproject.org/), et de [Tor](https://www.torproject.org/). Notre conception bénéficie considérablement de la recherche publiée à cette époque. I2P utilise plusieurs techniques d'onion routing, nous continuons donc à bénéficier de l'intérêt académique significatif pour Tor.

En s'appuyant sur les attaques et analyses présentées dans la [littérature sur l'anonymat](http://freehaven.net/anonbib/topic.html) (principalement [Traffic Analysis: Protocols, Attacks, Design Issues and Open Problems](http://citeseer.ist.psu.edu/454354.html)), ce qui suit décrit brièvement une grande variété d'attaques ainsi que de nombreuses défenses d'I2P. Nous mettons à jour cette liste pour inclure les nouvelles attaques au fur et à mesure qu'elles sont identifiées.

Sont incluses certaines attaques qui peuvent être propres à I2P. Nous n'avons pas de bonnes réponses à toutes ces attaques, cependant nous continuons à faire des recherches et à améliorer nos défenses.

De plus, bon nombre de ces attaques sont considérablement plus faciles qu'elles ne devraient l'être, en raison de la taille modeste du réseau actuel. Bien que nous soyons conscients de certaines limitations qui doivent être corrigées, I2P est conçu pour supporter des centaines de milliers, voire des millions, de participants. Alors que nous continuons à faire connaître le projet et à développer le réseau, ces attaques deviendront beaucoup plus difficiles.

Les pages de [comparaisons de réseaux](/docs/overview/comparison/) et de [terminologie "garlic"](/docs/overview/garlic-routing/) peuvent également être utiles à consulter.

### Attaques par force brute

Une attaque par force brute peut être menée par un adversaire passif ou actif global, surveillant tous les messages qui passent entre tous les nœuds et tentant de corréler quel message suit quel chemin. Monter cette attaque contre I2P devrait être non trivial, car tous les pairs du réseau envoient fréquemment des messages (à la fois des messages de bout en bout et de maintenance du réseau), et en plus un message de bout en bout change de taille et de données le long de son chemin. De plus, l'adversaire externe n'a pas non plus accès aux messages, car la communication inter-router est à la fois chiffrée et diffusée en flux (rendant deux messages de 1024 octets indiscernables d'un message de 2048 octets).

Cependant, un attaquant puissant peut utiliser la force brute pour détecter des tendances — s'il peut envoyer 5 Go vers une destination I2P et surveiller la connexion réseau de tout le monde, il peut éliminer tous les pairs qui n'ont pas reçu 5 Go de données. Des techniques pour contrer cette attaque existent, mais peuvent être d'un coût prohibitif (voir : les mimiques de [Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html) ou le trafic à débit constant). La plupart des utilisateurs ne s'inquiètent pas de cette attaque, car le coût de sa mise en œuvre est extrême (et nécessite souvent une activité illégale). Cependant, l'attaque reste possible, par exemple par un observateur chez un grand fournisseur d'accès Internet ou à un point d'échange Internet. Ceux qui veulent s'en défendre voudraient prendre des contre-mesures appropriées, comme fixer des limites de bande passante faibles, et utiliser des leasesets non publiés ou chiffrés pour les Sites I2P. D'autres contre-mesures, comme des délais non triviaux et des routes restreintes, ne sont actuellement pas implémentées.

Comme défense partielle contre un seul router ou un groupe de routers tentant d'acheminer tout le trafic du réseau, les routers contiennent des limites quant au nombre de tunnels qui peuvent être acheminés à travers un seul pair. À mesure que le réseau grandit, ces limites sont sujettes à des ajustements supplémentaires. D'autres mécanismes d'évaluation, de sélection et d'évitement des pairs sont discutés sur la page de sélection des pairs.

### Attaques temporelles

Les messages d'I2P sont unidirectionnels et n'impliquent pas nécessairement qu'une réponse sera envoyée. Cependant, les applications qui s'exécutent sur I2P auront très probablement des motifs reconnaissables dans la fréquence de leurs messages — par exemple, une requête HTTP sera un petit message suivi d'une grande séquence de messages de réponse contenant la réponse HTTP. En utilisant ces données ainsi qu'une vue d'ensemble de la topologie du réseau, un attaquant pourrait être capable de disqualifier certains liens comme étant trop lents pour avoir fait transiter le message.

Ce type d'attaque est puissant, mais son applicabilité à I2P n'est pas évidente, car la variation des délais de messages due à la mise en file d'attente, au traitement des messages et à la limitation du débit dépassera souvent ou égalera le temps de transmission d'un message le long d'un seul lien — même lorsque l'attaquant sait qu'une réponse sera envoyée dès que le message est reçu. Il existe cependant certains scénarios qui exposeront des réponses assez automatiques — la bibliothèque de streaming le fait (avec le SYN+ACK) tout comme le mode message de livraison garantie (avec le DataMessage+DeliveryStatusMessage).

Sans nettoyage de protocole ou latence plus élevée, les adversaires actifs globaux peuvent obtenir des informations substantielles. Ainsi, les personnes préoccupées par ces attaques pourraient augmenter la latence (en utilisant des délais non triviaux ou des stratégies de traitement par lots), inclure le nettoyage de protocole, ou d'autres techniques de routage de tunnel avancées, mais celles-ci ne sont pas implémentées dans I2P.

Références : [Low-Resource Routing Attacks Against Anonymous Systems](http://www.cs.colorado.edu/department/publications/reports/docs/CU-CS-1025-07.pdf)

### Attaques par intersection

Les attaques par intersection contre les systèmes à faible latence sont extrêmement puissantes — contactez périodiquement la cible et gardez une trace des pairs qui sont sur le réseau. Au fil du temps, lorsque le renouvellement des nœuds se produit, l'attaquant obtiendra des informations significatives sur la cible en intersectant simplement les ensembles de pairs qui sont en ligne lorsqu'un message passe avec succès. Le coût de cette attaque est important à mesure que le réseau grandit, mais peut être réalisable dans certains scénarios.

En résumé, si un attaquant se trouve aux deux extrémités de votre tunnel en même temps, il peut réussir. I2P n'a pas de défense complète contre cela pour les communications à faible latence. C'est une faiblesse inhérente du routage en oignon à faible latence. Tor fournit un [avertissement similaire](https://trac.torproject.org/projects/tor/wiki/TheOnionRouter/TorFAQ#Whatattacksremainagainstonionrouting).

Défenses partielles implémentées dans I2P :

- [Ordre strict](/docs/specs/tunnel-implementation/#ordering) des pairs
- Profilage et sélection des pairs à partir d'un petit groupe qui change lentement
- Limites sur le nombre de tunnels routés à travers un seul pair
- Prévention des pairs provenant de la même plage IP /16 d'être membres d'un seul tunnel
- Pour les sites I2P ou autres services hébergés, nous prenons en charge l'hébergement simultané sur plusieurs routers, ou multihoming

Même dans leur ensemble, ces défenses ne constituent pas une solution complète. De plus, nous avons fait certains choix de conception qui peuvent considérablement augmenter notre vulnérabilité :

- Nous n'utilisons pas de "guard nodes" à faible bande passante
- Nous utilisons des pools de tunnels composés de plusieurs tunnels, et le trafic peut passer d'un tunnel à l'autre.
- Les tunnels ne sont pas durables ; de nouveaux tunnels sont construits toutes les 10 minutes.
- Les longueurs de tunnel sont configurables. Bien que les tunnels à 3 sauts soient recommandés pour une protection complète, plusieurs applications et services utilisent des tunnels à 2 sauts par défaut.

À l'avenir, cela pourrait être possible pour les pairs qui peuvent se permettre des délais significatifs (selon des stratégies de délais non triviaux et de traitement par lots). De plus, ceci n'est pertinent que pour les destinations que d'autres personnes connaissent — un groupe privé dont la destination n'est connue que de pairs de confiance n'a pas à s'inquiéter, car un adversaire ne peut pas les "pinger" pour monter l'attaque.

Référence : [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)

### Attaques de déni de service

Il existe toute une série d'attaques par déni de service disponibles contre I2P, chacune avec des coûts et des conséquences différents :

**Attaque d'utilisateur gourmand :** Il s'agit simplement de personnes essayant de consommer significativement plus de ressources qu'elles ne sont disposées à contribuer. La défense contre cela est :

- Définir des paramètres par défaut pour que la plupart des utilisateurs fournissent des ressources au réseau. Dans I2P, les utilisateurs routent le trafic par défaut. En nette distinction avec [d'autres réseaux](/docs/overview/comparison/), plus de 95% des utilisateurs I2P relaient le trafic pour les autres.
- Fournir des options de configuration simples pour que les utilisateurs puissent augmenter leur contribution (pourcentage de partage) au réseau. Afficher des métriques faciles à comprendre comme le "ratio de partage" afin que les utilisateurs puissent voir ce qu'ils contribuent.
- Maintenir une communauté forte avec des blogs, des forums, IRC et d'autres moyens de communication.

**Attaque par famine :** Un utilisateur malveillant peut tenter de nuire au réseau en créant un nombre important de pairs dans le réseau qui ne sont pas identifiés comme étant sous le contrôle de la même entité (comme avec Sybil). Ces nœuds décident alors de ne fournir aucune ressource au réseau, obligeant les pairs existants à rechercher dans une base de données réseau plus large ou à demander plus de tunnels que nécessaire. Alternativement, les nœuds peuvent fournir un service intermittent en abandonnant périodiquement du trafic sélectionné, ou en refusant les connexions à certains pairs. Ce comportement peut être indiscernable de celui d'un nœud fortement chargé ou défaillant. I2P traite ces problèmes en maintenant des profils sur les pairs, en tentant d'identifier ceux qui sous-performent et en les ignorant simplement, ou en les utilisant rarement. Nous avons considérablement amélioré la capacité à reconnaître et éviter les pairs problématiques ; cependant des efforts significatifs sont encore nécessaires dans ce domaine.

**Attaque par inondation :** Un utilisateur malveillant peut tenter d'inonder le réseau, un pair, une destination, ou un tunnel. L'inondation du réseau et des pairs est possible, et I2P ne fait rien pour empêcher l'inondation standard au niveau de la couche IP. L'inondation d'une destination avec des messages en envoyant un grand nombre vers les diverses passerelles tunnel entrants de la cible est possible, mais la destination le saura à la fois par le contenu du message et parce que les tests du tunnel échoueront. Il en va de même pour l'inondation d'un seul tunnel. I2P n'a aucune défense contre une attaque d'inondation réseau. Pour une attaque d'inondation de destination et de tunnel, la cible identifie quels tunnels ne répondent pas et en construit de nouveaux. Du nouveau code pourrait également être écrit pour ajouter encore plus de tunnels si le client souhaite gérer la charge plus importante. Si, d'autre part, la charge est plus importante que ce que le client peut gérer, il peut demander aux tunnels de limiter le nombre de messages ou d'octets qu'ils doivent transmettre (une fois que l'opération avancée de tunnel est implémentée).

**Attaque par charge CPU :** Il existe actuellement certaines méthodes permettant aux utilisateurs de demander à distance qu'un pair effectue une opération cryptographiquement coûteuse, et un attaquant malveillant pourrait les utiliser pour inonder ce pair avec un grand nombre de ces demandes dans le but de surcharger le CPU. L'utilisation de bonnes pratiques d'ingénierie et potentiellement l'exigence de certificats non triviaux (par exemple HashCash) à joindre à ces demandes coûteuses devraient atténuer le problème, bien qu'il puisse y avoir de la place pour qu'un attaquant exploite diverses failles dans l'implémentation.

**Attaque DOS floodfill :** Un utilisateur hostile peut tenter de nuire au réseau en devenant un router floodfill. Les défenses actuelles contre les routers floodfill peu fiables, intermittents ou malveillants sont insuffisantes. Un router floodfill peut fournir des réponses erronées ou aucune réponse aux requêtes, et il peut également interférer avec la communication inter-floodfill. Certaines défenses et le profilage de pairs sont implémentés, cependant il reste beaucoup à faire. Pour plus d'informations, voir la [page de base de données réseau](/docs/specs/common-structures/).

### Attaques de marquage

Les attaques de marquage — modifier un message pour qu'il puisse être identifié plus tard le long du chemin — sont par elles-mêmes impossibles dans I2P, car les messages transmis à travers les tunnels sont signés. Cependant, si un attaquant est la passerelle du tunnel entrant ainsi qu'un participant plus loin dans ce tunnel, avec collusion ils peuvent identifier le fait qu'ils sont dans le même tunnel (et avant l'ajout d'identifiants de saut uniques et d'autres mises à jour, les pairs colludeurs au sein du même tunnel peuvent reconnaître ce fait sans aucun effort). Un attaquant dans un tunnel sortant et toute partie d'un tunnel entrant ne peuvent cependant pas colluder, car le chiffrement du tunnel remplit et modifie les données séparément pour les tunnels entrants et sortants. Les attaquants externes ne peuvent rien faire, car les liens sont chiffrés et les messages signés.

### Attaques de partitionnement

Les attaques de partitionnement — trouver des moyens de séparer (techniquement ou analytiquement) les pairs dans un réseau — sont importantes à garder à l'esprit lorsqu'on fait face à un adversaire puissant, car la taille du réseau joue un rôle clé dans la détermination de votre anonymat. Le partitionnement technique par coupure des liens entre pairs pour créer des réseaux fragmentés est traité par la netDb intégrée d'I2P, qui maintient des statistiques sur divers pairs afin de permettre d'exploiter toute connexion existante vers d'autres sections fragmentées dans le but de réparer le réseau. Cependant, si l'attaquant déconnecte effectivement tous les liens vers les pairs non contrôlés, isolant essentiellement la cible, aucune réparation par netDb ne pourra y remédier. À ce moment-là, la seule chose que le router peut espérer faire est de remarquer qu'un nombre significatif de pairs précédemment fiables sont devenus indisponibles et alerter le client qu'il est temporairement déconnecté (ce code de détection n'est pas implémenté pour le moment).

Le partitionnement analytique du réseau en recherchant les différences dans le comportement des routers et des destinations et en les regroupant en conséquence constitue également une attaque très puissante. Par exemple, un attaquant [récoltant](#harvesting-attacks) la base de données réseau saura quand une destination particulière a 5 tunnels entrants dans son LeaseSet alors que d'autres n'en ont que 2 ou 3, permettant à l'adversaire de potentiellement partitionner les clients selon le nombre de tunnels sélectionnés. Un autre partitionnement est possible lors du traitement de délais non triviaux et de stratégies de traitement par lots, car les passerelles de tunnel et les sauts particuliers avec des délais non nuls se démarqueront probablement. Cependant, ces données ne sont exposées qu'à ces sauts spécifiques, donc pour partitionner efficacement sur cette base, l'attaquant devrait contrôler une portion significative du réseau (et même ainsi, ce ne serait qu'un partitionnement probabiliste, car il ne saurait pas quels autres tunnels ou messages ont ces délais).

Également discuté sur la [page de la base de données réseau](/docs/specs/common-structures/) (attaque de bootstrap).

### Attaques de prédécesseur

L'attaque du prédécesseur consiste à collecter passivement des statistiques dans le but de voir quels pairs sont « proches » de la destination en participant à leurs tunnels et en suivant le saut précédent ou suivant (pour les tunnels sortants ou entrants, respectivement). Au fil du temps, en utilisant un échantillon parfaitement aléatoire de pairs et un ordre aléatoire, un attaquant pourrait voir quel pair apparaît comme « plus proche » statistiquement plus que les autres, et ce pair serait à son tour l'endroit où se trouve la cible.

I2P évite cela de quatre façons : premièrement, les pairs sélectionnés pour participer aux tunnels ne sont pas échantillonnés de manière aléatoire dans tout le réseau — ils sont dérivés de l'algorithme de sélection des pairs qui les divise en niveaux. Deuxièmement, avec l'[ordre strict](/docs/specs/tunnel-implementation/#ordering) des pairs dans un tunnel, le fait qu'un pair apparaisse plus fréquemment ne signifie pas qu'il soit la source. Troisièmement, avec la longueur de tunnel permutée (non activée par défaut), même les tunnels à 0 saut peuvent fournir un déni plausible car la variation occasionnelle de la passerelle ressemblera à des tunnels normaux. Quatrièmement, avec les routes restreintes (non implémentées), seul le pair avec une connexion restreinte vers la cible contactera jamais la cible, tandis que les attaquants ne feront que se heurter à cette passerelle.

La méthode actuelle de construction de tunnel a été spécifiquement conçue pour contrer l'attaque du prédécesseur. Voir aussi [l'attaque par intersection](#intersection-attacks).

Références : [Wright et al. 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf), qui est une mise à jour de l'[article d'attaque précédent de 2004](http://forensics.umass.edu/pubs/wright-tissec.pdf).

### Attaques de collecte

Le "Harvesting" (collecte de données) signifie compiler une liste d'utilisateurs exécutant I2P. Il peut être utilisé pour des attaques légales et pour aider d'autres attaques en exécutant simplement un pair, en voyant à qui il se connecte, et en collectant toutes les références à d'autres pairs qu'il peut trouver.

I2P lui-même n'est pas conçu avec des défenses efficaces contre cette attaque, puisqu'il existe la base de données réseau distribuée contenant précisément cette information. Les facteurs suivants rendent l'attaque quelque peu plus difficile en pratique :

- La croissance du réseau rendra plus difficile l'obtention d'une proportion donnée du réseau
- Les routeurs floodfill implémentent des limites de requêtes comme protection contre les attaques DOS
- Le "mode caché", qui empêche un router de publier ses informations dans la netDb, (mais l'empêche aussi de relayer des données) n'est pas largement utilisé maintenant mais pourrait l'être.

Dans les implémentations futures, les routes restreintes basiques et complètes réduiraient la puissance de cette attaque, car les pairs "cachés" ne publient pas leurs adresses de contact dans la base de données réseau — seulement les tunnels par lesquels ils peuvent être atteints (ainsi que leurs clés publiques, etc).

À l'avenir, les routers pourraient utiliser GeoIP pour identifier s'ils se trouvent dans un pays particulier où l'identification en tant que nœud I2P serait risquée. Dans ce cas, le router pourrait automatiquement activer le mode masqué, ou mettre en œuvre d'autres méthodes de routage restreintes.

### Identification par analyse de trafic

En inspectant le trafic entrant et sortant d'un router, un FAI malveillant ou un pare-feu étatique pourrait identifier qu'un ordinateur exécute I2P. Comme discuté [ci-dessus](#harvesting-attacks), I2P n'est pas spécifiquement conçu pour masquer qu'un ordinateur exécute I2P. Cependant, plusieurs décisions de conception prises dans la conception de la couche transport et des protocoles rendent quelque peu difficile l'identification du trafic I2P :

- Sélection de port aléatoire
- Chiffrement point-à-point de tout le trafic
- Échange de clés DH sans octets de protocole ou autres champs constants non chiffrés
- Utilisation simultanée des transports TCP et UDP. L'UDP peut être beaucoup plus difficile à suivre pour certains équipements d'inspection approfondie des paquets (DPI).

Dans un avenir proche, nous prévoyons d'aborder directement les problèmes d'analyse de trafic en obfusquant davantage les protocoles de transport I2P, incluant possiblement :

- Remplissage au niveau de la couche transport vers des longueurs aléatoires, surtout durant la négociation de connexion
- Étude des signatures de distribution de taille de paquets, et remplissage supplémentaire si nécessaire
- Développement de méthodes de transport supplémentaires qui imitent SSL ou d'autres protocoles courants
- Révision des stratégies de remplissage aux couches supérieures pour voir comment elles affectent les tailles de paquets au niveau de la couche transport
- Révision des méthodes implémentées par divers pare-feu étatiques pour bloquer Tor
- Travail direct avec les experts en DPI (inspection approfondie de paquets) et obfuscation

Référence : [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)

### Attaques Sybil

Sybil décrit une catégorie d'attaques où l'adversaire crée un nombre arbitrairement important de nœuds collaborateurs et utilise cette augmentation pour faciliter d'autres attaques. Par exemple, si un attaquant se trouve dans un réseau où les pairs sont sélectionnés aléatoirement et qu'il souhaite avoir 80% de chances d'être l'un de ces pairs, il lui suffit de créer cinq fois le nombre de nœuds présents dans le réseau et de tenter sa chance. Lorsque l'identité est gratuite, Sybil peut être une technique très puissante pour un adversaire disposant de moyens importants. La technique principale pour contrer cela consiste simplement à rendre l'identité 'non gratuite' — [Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (entre autres) utilise le fait que les adresses IP sont limitées, tandis qu'IIP utilisait [HashCash](http://www.hashcash.org/) pour 'facturer' la création d'une nouvelle identité. Nous n'avons actuellement implémenté aucune technique particulière pour traiter Sybil, mais nous incluons des certificats de substitution dans les structures de données du router et de la destination qui peuvent contenir un certificat HashCash de valeur appropriée lorsque nécessaire (ou un autre certificat prouvant la rareté).

Exiger des certificats HashCash à divers endroits présente deux problèmes majeurs :

- Maintenir la compatibilité ascendante
- Le problème classique de HashCash — sélectionner des valeurs HashCash qui constituent des preuves de travail significatives sur les machines haut de gamme, tout en restant réalisables sur les machines bas de gamme comme les appareils mobiles.

Diverses limitations sur le nombre de routers dans une plage IP donnée restreignent la vulnérabilité aux attaquants qui n'ont pas la capacité de placer des machines dans plusieurs blocs IP. Cependant, cela ne constitue pas une défense significative contre un adversaire puissant.

Voir la [page de la base de données réseau](/docs/specs/common-structures/) pour plus de discussion sur les attaques Sybil.

### Attaques d'épuisement de pairs

(Référence : [In Search of an Anonymous and Secure Lookup](http://www.eecs.berkeley.edu/~pmittal/publications/nisan-torsk-ccs10.pdf) Section 5.2)

En refusant d'accepter ou de transmettre les demandes de construction de tunnel, sauf vers un pair complice, un router pourrait s'assurer qu'un tunnel soit formé entièrement à partir de son ensemble de routers complices. Les chances de succès sont renforcées s'il y a un grand nombre de routers complices, c'est-à-dire une [attaque Sybil](#sybil-attacks). Ceci est quelque peu atténué par nos méthodes de profilage de pairs utilisées pour surveiller les performances des pairs. Cependant, il s'agit d'une attaque puissante lorsque le nombre de routers approche *f* = 0,2, ou 20 % de nœuds malveillants, comme spécifié dans l'article. Les routers malveillants pourraient également maintenir des connexions vers le router cible et fournir une excellente bande passante de transmission pour le trafic sur ces connexions, dans une tentative de manipuler les profils gérés par la cible et paraître attractifs. Des recherches et défenses supplémentaires peuvent être nécessaires.

### Attaques cryptographiques

Nous utilisons une cryptographie forte avec des clés longues, et nous supposons la sécurité des primitives cryptographiques standard de l'industrie utilisées dans I2P. Les fonctionnalités de sécurité incluent la détection immédiate des messages altérés le long du chemin, l'impossibilité de déchiffrer les messages qui ne vous sont pas adressés, et la défense contre les attaques de l'homme du milieu. Les tailles de clés choisies en 2003 étaient assez conservatrices à l'époque, et sont encore plus longues que celles utilisées dans [d'autres réseaux d'anonymat](https://torproject.org/). Nous ne pensons pas que les longueurs de clés actuelles soient notre plus grande faiblesse, en particulier pour les adversaires traditionnels, non étatiques ; les bogues et la petite taille du réseau sont beaucoup plus préoccupants. Bien sûr, tous les algorithmes cryptographiques deviennent finalement obsolètes en raison de l'avènement de processeurs plus rapides, de la recherche cryptographique, et des avancées dans des méthodes telles que les tables arc-en-ciel, les grappes de matériel de jeux vidéo, etc. Malheureusement, I2P n'a pas été conçu avec des mécanismes faciles pour allonger les clés ou changer les valeurs secrètes partagées tout en maintenant la compatibilité descendante.

La mise à niveau des diverses structures de données et protocoles pour prendre en charge des clés plus longues devra être abordée à terme, et ce sera un projet majeur, tout comme ce le sera pour [d'autres](https://torproject.org/). Espérons que, grâce à une planification minutieuse, nous pourrons minimiser les perturbations et implémenter des mécanismes pour faciliter les transitions futures.

À l'avenir, plusieurs protocoles I2P et structures de données prendront en charge le remplissage sécurisé des messages à des tailles arbitraires, de sorte que les messages pourraient être rendus de taille constante ou les garlic messages pourraient être modifiés de manière aléatoire afin que certains cloves semblent contenir plus de sous-cloves qu'ils n'en contiennent réellement. Pour le moment, cependant, les messages garlic, tunnel et de bout en bout incluent un simple remplissage aléatoire.

### Attaques d'anonymat floodfill

En plus des attaques DOS contre les floodfill décrites [ci-dessus](#denial-of-service-attacks), les routeurs floodfill sont dans une position unique pour apprendre des informations sur les participants du réseau, en raison de leur rôle dans le netDb et de la haute fréquence de communication avec ces participants. Ceci est quelque peu atténué car les routeurs floodfill ne gèrent qu'une portion de l'espace de clés total, et l'espace de clés effectue une rotation quotidienne, comme expliqué sur la [page de base de données réseau](/docs/specs/common-structures/). Les mécanismes spécifiques par lesquels les routeurs communiquent avec les floodfill ont été soigneusement conçus. Cependant, ces menaces devraient être étudiées plus en détail. Les menaces potentielles spécifiques et les défenses correspondantes constituent un sujet de recherche future.

### Autres attaques de la base de données réseau

Un utilisateur malveillant peut tenter de nuire au réseau en créant un ou plusieurs routeurs floodfill et en les configurant pour offrir des réponses incorrectes, lentes ou inexistantes. Plusieurs scénarios sont discutés sur la [page de la base de données réseau](/docs/specs/common-structures/).

### Attaques sur les ressources centrales

Il existe quelques ressources centralisées ou limitées (certaines à l'intérieur d'I2P, d'autres non) qui pourraient être attaquées ou utilisées comme vecteur d'attaques. L'absence de jrandom à partir de novembre 2007, suivie de la perte du service d'hébergement i2p.net en janvier 2008, a mis en évidence de nombreuses ressources centralisées dans le développement et le fonctionnement du réseau I2P, dont la plupart sont maintenant distribuées. Les attaques sur les ressources accessibles de l'extérieur affectent principalement la capacité des nouveaux utilisateurs à nous trouver, pas le fonctionnement du réseau lui-même.

- Le site web est mis en miroir et utilise le DNS round-robin pour l'accès public externe.
- Les routeurs prennent désormais en charge [plusieurs emplacements externes de reseed](/docs/overview/faq/#reseed), cependant davantage d'hôtes reseed peuvent être nécessaires, et la gestion des hôtes reseed peu fiables ou malveillants peut nécessiter des améliorations.
- Les routeurs prennent désormais en charge plusieurs emplacements de fichiers de mise à jour. Un hôte de mise à jour malveillant pourrait fournir un fichier énorme ; il faut limiter la taille.
- Les routeurs prennent désormais en charge plusieurs signataires de confiance par défaut pour les mises à jour.
- Les routeurs gèrent désormais mieux plusieurs pairs floodfill peu fiables. Les floodfills malveillants nécessitent davantage d'étude.
- Le code est maintenant stocké dans un système de contrôle de source distribué.
- Les routeurs dépendent d'un seul hôte de nouvelles, mais il existe une URL de sauvegarde codée en dur pointant vers un hôte différent. Un hôte de nouvelles malveillant pourrait fournir un fichier énorme ; il faut limiter la taille.
- [Les services du système de nommage](/docs/overview/naming/), y compris les fournisseurs d'abonnements de carnet d'adresses, les services d'ajout d'hôtes et les services de saut, peuvent être malveillants. Des protections substantielles pour les abonnements ont été implémentées dans la version 0.6.1.31, avec des améliorations supplémentaires dans les versions ultérieures. Cependant, tous les services de nommage nécessitent une certaine mesure de confiance ; voir [la page de nommage](/docs/overview/naming/) pour plus de détails.
- Nous restons dépendants du service DNS pour i2p2.de ; perdre ceci causerait une perturbation substantielle dans notre capacité à attirer de nouveaux utilisateurs, et réduirait le réseau (à court et moyen terme), tout comme la perte d'i2p.net l'a fait.

### Attaques de développement

Ces attaques ne visent pas directement le réseau, mais s'en prennent plutôt à son équipe de développement en introduisant soit des obstacles juridiques pour quiconque contribue au développement du logiciel, soit en utilisant tous les moyens disponibles pour amener les développeurs à subvertir le logiciel. Les mesures techniques traditionnelles ne peuvent pas contrer ces attaques, et si quelqu'un menaçait la vie ou les moyens de subsistance d'un développeur (ou même en émettant simplement une ordonnance judiciaire accompagnée d'une ordonnance de non-divulgation, sous peine d'emprisonnement), nous aurions un gros problème.

Cependant, deux techniques aident à se défendre contre ces attaques :

- Tous les composants du réseau doivent être open source pour permettre l'inspection, la vérification, la modification et l'amélioration. Si un développeur est compromis, une fois que cela est remarqué, la communauté devrait exiger des explications et cesser d'accepter le travail de ce développeur. Tous les commits vers notre système de contrôle de version distribué sont signés cryptographiquement, et les responsables des versions utilisent un système de liste de confiance pour restreindre les modifications à celles préalablement approuvées.
- Développement sur le réseau lui-même, permettant aux développeurs de rester anonymes tout en sécurisant le processus de développement. Tout le développement I2P peut se faire à travers I2P — en utilisant un système de contrôle de version distribué, le chat IRC, des serveurs web publics, des forums de discussion (forum.i2p), et les sites de distribution de logiciels, tous disponibles dans I2P.

Nous entretenons également des relations avec diverses organisations qui offrent des conseils juridiques, au cas où une défense serait nécessaire.

### Attaques d'implémentation (Bugs)

Malgré tous nos efforts, la plupart des applications non triviales comportent des erreurs de conception ou d'implémentation, et I2P ne fait pas exception. Il peut y avoir des bogues qui pourraient être exploités pour attaquer l'anonymat ou la sécurité de la communication s'exécutant sur I2P de manière inattendue. Pour aider à résister aux attaques contre la conception ou les protocoles utilisés, nous publions toutes les conceptions et documentations et sollicitons des révisions et des critiques dans l'espoir que de nombreux regards amélioreront le système. Nous ne croyons pas en la sécurité par l'obscurité.

De plus, le code est traité de la même manière, avec peu de réticence à retravailler ou à abandonner quelque chose qui ne répond pas aux besoins du système logiciel (y compris la facilité de modification). La documentation de la conception et de l'implémentation du réseau et des composants logiciels est un élément essentiel de la sécurité, car sans elle, il est peu probable que les développeurs soient disposés à consacrer le temps nécessaire pour apprendre suffisamment le logiciel afin d'identifier les lacunes et les bogues.

Notre logiciel est susceptible, en particulier, de contenir des bogues liés au déni de service par des erreurs de mémoire insuffisante (OOM), des problèmes de script inter-sites (XSS) dans la console du router, et d'autres vulnérabilités aux entrées non standard via les différents protocoles.

I2P reste un petit réseau avec une petite communauté de développement et presque aucun intérêt de la part de groupes académiques ou de recherche. Par conséquent, il nous manque l'analyse que [d'autres réseaux d'anonymat](https://torproject.org/) ont pu recevoir. Nous continuons à recruter des personnes pour [s'impliquer](/get-involved/) et nous aider.

---

## Autres défenses

### Listes de blocage

Dans une certaine mesure, I2P pourrait être amélioré pour éviter les pairs opérant à des adresses IP listées dans une liste de blocage. Plusieurs listes de blocage sont couramment disponibles dans des formats standard, répertoriant les organisations anti-P2P, les adversaires potentiels au niveau étatique, et d'autres.

Dans la mesure où les pairs actifs apparaissent effectivement dans la liste de blocage réelle, le blocage par seulement un sous-ensemble de pairs aurait tendance à segmenter le réseau, à exacerber les problèmes d'accessibilité et à diminuer la fiabilité globale. Par conséquent, nous voudrions nous accorder sur une liste de blocage particulière et l'activer par défaut.

Les listes de blocage ne constituent qu'une partie (peut-être une petite partie) d'un ensemble de défenses contre la malveillance. En grande partie, le système de profilage fait du bon travail pour mesurer le comportement des router afin que nous n'ayons pas besoin de faire confiance à quoi que ce soit dans netDb. Cependant, il y a plus qui peut être fait. Pour chacun des domaines de la liste ci-dessus, nous pouvons apporter des améliorations dans la détection de la malveillance.

Si une liste de blocage est hébergée dans un emplacement central avec des mises à jour automatiques, le réseau est vulnérable à une [attaque de ressource centrale](#central-resource-attacks). L'abonnement automatique à une liste donne au fournisseur de la liste le pouvoir d'arrêter complètement le réseau I2P.

Actuellement, une liste de blocage par défaut est distribuée avec notre logiciel, répertoriant uniquement les adresses IP de sources de DOS passées. Il n'existe aucun mécanisme de mise à jour automatique. Si une plage d'adresses IP particulière mettait en œuvre des attaques sérieuses contre le réseau I2P, nous devrions demander aux utilisateurs de mettre à jour leur liste de blocage manuellement par le biais de mécanismes hors bande tels que les forums, blogs, etc.
