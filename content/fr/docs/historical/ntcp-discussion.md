---
title: "Discussion NTCP"
description: "Discussion historique sur les protocoles de transport NTCP vs SSU de mars 2007"
slug: "ntcp-discussion"
aliases:
  - "/fr/docs/discussions/ntcp"
  - "/fr/docs/discussions/ntcp/"
  - "/fr/ntcp_discussion"
  - "/fr/ntcp_discussion/"
lastUpdated: "2007-03"
accurateFor: "historical"
---

Ce qui suit est une discussion sur NTCP qui a eu lieu en mars 2007. Elle n'a pas été mise à jour pour refléter l'implémentation actuelle. Pour la spécification NTCP actuelle, voir [la page NTCP2](/docs/specs/ntcp2).

## Discussion NTCP vs. SSU, Mars 2007 {#ntcp-ssu}

### Questions NTCP

(adapté d'une discussion IRC entre zzz et cervantes)

Pourquoi NTCP est-il préféré à SSU, NTCP n'a-t-il pas une surcharge et une latence plus élevées ? Il a une meilleure fiabilité.

La bibliothèque de streaming sur NTCP ne souffre-t-elle pas des problèmes classiques TCP-sur-TCP ? Et si nous avions un transport UDP vraiment simple pour le trafic provenant de la bibliothèque de streaming ? Je pense que SSU était censé être ce transport UDP soi-disant vraiment simple - mais il s'est avéré tout simplement trop peu fiable.

### Analyse "NTCP Considered Harmful" par zzz {#harmful}

Publié sur le nouveau Syndie, 2007-03-25. Ceci a été publié pour stimuler la discussion, ne le prenez pas trop au sérieux.

**Résumé :** NTCP présente une latence et une surcharge plus élevées que SSU, et est plus susceptible de s'effondrer lorsqu'il est utilisé avec la bibliothèque de streaming. Cependant, le trafic est acheminé avec une préférence pour NTCP plutôt que SSU et ceci est actuellement codé en dur.

#### Discussion

Nous avons actuellement deux transports, NTCP et SSU. Tels qu'implémentés actuellement, NTCP a des "enchères" plus faibles que SSU donc il est privilégié, sauf dans le cas où il existe une connexion SSU établie mais aucune connexion NTCP établie pour un pair.

SSU est similaire à NTCP en ce qu'il implémente les accusés de réception, les timeouts et les retransmissions. Cependant SSU est du code I2P avec des contraintes strictes sur les timeouts et des statistiques disponibles sur les temps de trajet aller-retour, les retransmissions, etc. NTCP est basé sur Java NIO TCP, qui est une boîte noire et implémente vraisemblablement les standards RFC, incluant des timeouts maximum très longs.

La majorité du trafic dans I2P provient de streaming-lib (HTTP, IRC, Bittorrent) qui est notre implémentation de TCP. Comme le transport de niveau inférieur est généralement NTCP en raison des enchères plus basses, le système est sujet au problème bien connu et redoutable du TCP-over-TCP http://sites.inka.de/~W1011/devel/tcp-tcp.html , où les couches TCP supérieures et inférieures effectuent des retransmissions simultanément, entraînant un effondrement.

Contrairement au scénario PPP over SSH décrit dans le lien ci-dessus, nous avons plusieurs sauts pour la couche inférieure, chacun couvert par une liaison NTCP. Ainsi, chaque latence NTCP est généralement bien inférieure à la latence de la bibliothèque de streaming de couche supérieure. Cela réduit les risques d'effondrement.

De plus, les probabilités d'effondrement sont réduites lorsque le TCP de couche inférieure est strictement contraint avec des délais d'attente faibles et un nombre limité de retransmissions par rapport à la couche supérieure.

La version .28 a augmenté le délai d'attente maximal de la bibliothèque de streaming de 10 sec à 45 sec, ce qui a grandement amélioré les choses. Le délai d'attente maximal SSU est de 3 sec. Le délai d'attente maximal NTCP est probablement d'au moins 60 sec, ce qui correspond à la recommandation RFC. Il n'y a aucun moyen de modifier les paramètres NTCP ou de surveiller les performances. L'effondrement de la couche NTCP est [éditeur : texte perdu]. Peut-être qu'un outil externe comme tcpdump pourrait aider.

Cependant, en exécutant la version .28, le débit montant rapporté par i2psnark ne reste généralement pas à un niveau élevé. Il descend souvent à 3-4 KBps avant de remonter. C'est un signal qu'il y a encore des effondrements.

SSU est également plus efficace. NTCP a une surcharge plus élevée et probablement des temps d'aller-retour plus longs. Lors de l'utilisation de NTCP, le ratio de (sortie de tunnel) / (sortie de données i2psnark) est d'au moins 3,5 : 1. En exécutant une expérience où le code a été modifié pour préférer SSU (l'option de configuration i2np.udp.alwaysPreferred n'a aucun effet dans le code actuel), le ratio a été réduit à environ 3 : 1, indiquant une meilleure efficacité.

Comme le rapportent les statistiques de la bibliothèque de streaming, les choses se sont nettement améliorées - la taille de fenêtre de durée de vie est passée de 6,3 à 7,5, le RTT est descendu de 11,5s à 10s, les envois par accusé de réception sont passés de 1,11 à 1,07.

Que cela ait été si efficace était surprenant, étant donné que nous ne changions que le transport pour le premier des 3 à 5 hops au total que prendraient les messages sortants.

L'effet sur les vitesses sortantes d'i2psnark n'était pas clair en raison des variations normales. De plus, pour l'expérience, le NTCP entrant était désactivé. L'effet sur les vitesses entrantes d'i2psnark n'était pas clair.

#### Propositions

1. **1A)** C'est facile -
   Nous devrions inverser les priorités d'enchères pour que SSU soit préféré pour tout le trafic, si
   nous pouvons le faire sans causer toutes sortes d'autres problèmes. Cela corrigera l'option
   de configuration i2np.udp.alwaysPreferred pour qu'elle fonctionne (soit comme true
   ou false).

2. **1B)** Alternative à 1A), pas si facile -
   Si nous pouvons marquer le trafic sans affecter négativement nos objectifs d'anonymat, nous
   devrions identifier le trafic généré par streaming-lib et faire en sorte que SSU génère une offre faible
   pour ce trafic. Cette balise devra accompagner le message à travers chaque saut
   afin que les routeurs de transfert honorent également la préférence SSU.

3. **2)** Limiter SSU encore davantage (en réduisant les retransmissions maximales par rapport aux 10 actuelles) est probablement judicieux pour réduire les risques d'effondrement.

4. **3)** Nous avons besoin d'une étude plus approfondie sur les avantages par rapport aux inconvénients d'un protocole semi-fiable sous-jacent à la bibliothèque de streaming. Les retransmissions sur un seul saut sont-elles bénéfiques et représentent-elles un gros avantage ou sont-elles pires qu'inutiles ?
   Nous pourrions créer un nouveau SUU (UDP non fiable sécurisé) mais ce n'est probablement pas la peine. Nous pourrions peut-être ajouter un type de message sans accusé de réception requis dans SSU si nous ne voulons aucune retransmission du trafic de la bibliothèque de streaming. Les retransmissions étroitement délimitées sont-elles souhaitables ?

5. **4)** Le code d'envoi prioritaire dans .28 est uniquement pour NTCP. Jusqu'à présent, mes tests n'ont pas montré beaucoup d'utilité pour la priorité SSU car les messages ne se mettent pas assez longtemps en file d'attente pour que les priorités soient utiles. Mais davantage de tests sont nécessaires.

6. **5)** Le nouveau timeout maximum de 45s de la bibliothèque de streaming est probablement encore trop faible.
   Le RFC TCP indique 60s. Il ne devrait probablement pas être plus court que le timeout maximum NTCP sous-jacent (vraisemblablement 60s).

### Réponse de jrandom {#jrandom-response}

Publié sur le nouveau Syndie, 2007-03-27

Dans l'ensemble, je suis ouvert à l'expérimentation avec ceci, mais rappelons-nous pourquoi NTCP est là en premier lieu - SSU a échoué dans un effondrement de congestion. NTCP "fonctionne tout simplement", et bien que des taux de retransmission de 2-10% puissent être gérés dans des réseaux normaux à saut unique, cela nous donne un taux de retransmission de 40% avec des tunnels à 2 sauts. Si vous incluez certains des taux de retransmission SSU mesurés que nous avions vus avant l'implémentation de NTCP (10-30+%), cela nous donne un taux de retransmission de 83%. Peut-être que ces taux étaient causés par le faible délai d'expiration de 10 secondes, mais l'augmenter autant nous pénaliserait (rappelez-vous, multipliez par 5 et vous avez la moitié du voyage).

Contrairement à TCP, nous n'avons aucun retour du tunnel pour savoir si le message est arrivé - il n'y a pas d'accusés de réception au niveau du tunnel. Nous avons bien des ACK de bout en bout, mais seulement sur un petit nombre de messages (chaque fois que nous distribuons de nouvelles balises de session) - sur les 1 553 591 messages client que mon router a envoyés, nous n'avons tenté d'obtenir un ACK que pour 145 207 d'entre eux. Les autres ont peut-être échoué silencieusement ou réussi parfaitement.

Je ne suis pas convaincu par l'argument TCP-over-TCP pour nous, surtout réparti sur les différents chemins par lesquels nous transférons. Des mesures sur I2P peuvent bien sûr me convaincre du contraire.

> *Le délai d'expiration maximum NTCP est vraisemblablement d'au moins 60 sec, ce qui est la recommandation RFC. Il n'y a aucun moyen de modifier les paramètres NTCP ou de surveiller les performances.*

C'est vrai, mais les connexions réseau n'atteignent ce niveau que lorsque quelque chose de vraiment grave se produit - le délai de retransmission TCP est souvent de l'ordre de dizaines ou centaines de millisecondes. Comme le souligne foofighter, ils ont plus de 20 ans d'expérience et de correction de bogues dans leurs piles TCP, plus une industrie de milliards de dollars qui optimise le matériel et les logiciels pour bien fonctionner selon ce qu'ils font.

> *NTCP a une surcharge plus élevée et probablement des temps d'aller-retour plus longs. lors de l'utilisation de NTCP > le rapport de (sortie tunnel) / (sortie données i2psnark) est d'au moins 3,5 : 1. > En exécutant une expérience où le code a été modifié pour préférer SSU (l'option de configuration > i2np.udp.alwaysPreferred n'a aucun effet dans le code actuel), le rapport > a été réduit à environ 3 : 1, indiquant une meilleure efficacité.*

Ces données sont très intéressantes, bien que davantage en tant que question de congestion du router que d'efficacité de bande passante - il faudrait comparer 3.5*$n*$NTCPRetransmissionPct ./. 3.0*$n*$SSURetransmissionPct. Ce point de données suggère qu'il y a quelque chose dans le router qui conduit à une mise en file d'attente locale excessive des messages déjà en cours de transfert.

> *taille de fenêtre de durée de vie augmentée de 6,3 à 7,5, RTT réduit de 11,5s à 10s, envois par > ACK réduit de 1,11 à 1,07.*

Rappelez-vous que les envois-par-ACK ne constituent qu'un échantillon et non un décompte complet (car nous n'essayons pas d'acquitter chaque envoi). Ce n'est pas non plus un échantillon aléatoire, mais il échantillonne plus lourdement les périodes d'inactivité ou l'initiation d'un pic d'activité - une charge soutenue ne nécessitera pas beaucoup d'ACK.

Les tailles de fenêtre dans cette plage restent dramatiquement faibles pour obtenir le véritable bénéfice d'AIMD, et encore trop faibles pour transmettre un seul chunk BT de 32 Ko (augmenter le plancher à 10 ou 12 couvrirait cela).

Néanmoins, la statistique wsize semble prometteuse - pendant combien de temps a-t-elle été maintenue ?

En fait, à des fins de test, vous voudrez peut-être examiner StreamSinkClient/StreamSinkServer ou même TestSwarm dans apps/ministreaming/java/src/net/i2p/client/streaming/ - StreamSinkClient est une application CLI qui envoie un fichier sélectionné vers une destination sélectionnée et StreamSinkServer crée une destination et écrit toutes les données qui lui sont envoyées (affichant la taille et le temps de transfert). TestSwarm combine les deux - inondant de données aléatoires tous ceux auxquels il se connecte. Cela devrait vous donner les outils pour mesurer la capacité de débit soutenu sur la bibliothèque de streaming, par opposition au mécanisme choke/send de BT.

> *1A) C'est facile - > Nous devrions inverser les priorités d'offre pour que SSU soit préféré pour tout le trafic, si > nous pouvons faire cela sans causer toutes sortes d'autres problèmes. Cela corrigera l'> option de configuration i2np.udp.alwaysPreferred pour qu'elle fonctionne (soit comme true > ou false).*

Respecter i2np.udp.alwaysPreferred est une bonne idée dans tous les cas - n'hésitez pas à valider ce changement. Rassemblons cependant un peu plus de données avant de changer les préférences, car NTCP a été ajouté pour gérer un effondrement de congestion créé par SSU.

> *1B) Alternative à 1A), pas si facile - > Si nous pouvons marquer le trafic sans affecter négativement nos objectifs d'anonymat, nous > devons identifier le trafic généré par streaming-lib > et faire en sorte que SSU génère une offre faible pour ce trafic. Cette balise devra accompagner > le message à travers chaque saut > afin que les routeurs de retransmission honorent également la préférence SSU.*

En pratique, il existe trois types de trafic - construction/test de tunnel, requête/réponse netDb, et trafic de bibliothèque de streaming. Le réseau a été conçu pour rendre la différenciation de ces trois types très difficile.

> *2) Limiter davantage SSU (en réduisant le nombre maximum de retransmissions par rapport aux > 10 actuelles) est probablement sage pour réduire le risque d'effondrement.*

Avec 10 retransmissions, on est déjà dans de beaux draps, je suis d'accord. Une, peut-être deux retransmissions sont raisonnables, du point de vue de la couche transport, mais si l'autre côté est trop congestionné pour acquitter à temps (même avec la capacité SACK/NACK implémentée), il n'y a pas grand-chose que nous puissions faire.

À mon avis, pour vraiment résoudre le problème fondamental, nous devons nous pencher sur les raisons pour lesquelles le router devient si congestionné qu'il ne peut pas ACK à temps (ce qui, d'après ce que j'ai trouvé, est dû à la contention CPU). Peut-être pouvons-nous réorganiser certaines choses dans le traitement du router pour donner une priorité CPU plus élevée à la transmission d'un tunnel existant par rapport au déchiffrement d'une nouvelle demande de tunnel ? Mais nous devons faire attention à éviter la famine.

> *3) Nous avons besoin d'une étude plus approfondie sur les avantages par rapport aux inconvénients d'un protocole semi-fiable > sous-jacent à la bibliothèque de streaming. Les retransmissions sur un seul saut sont-elles bénéfiques > et constituent-elles un gros avantage ou sont-elles pires qu'inutiles ? > Nous pourrions créer un nouveau SUU (UDP sécurisé non fiable) mais cela n'en vaut probablement pas la peine. Nous > pourrions peut-être ajouter un type de message sans ACK requis dans SSU si nous ne voulons aucune > retransmission du tout pour le trafic de la bibliothèque de streaming. Les > retransmissions strictement délimitées sont-elles souhaitables ?*

Cela vaut la peine d'être étudié - et si nous désactivions simplement les retransmissions de SSU ? Cela conduirait probablement à des taux de renvoi beaucoup plus élevés dans la bibliothèque de streaming, mais peut-être pas.

> *4) Le code d'envoi prioritaire dans .28 est uniquement pour NTCP. Jusqu'à présent, mes tests n'ont pas montré beaucoup d'utilité pour la priorité SSU car les messages ne restent pas assez longtemps en file d'attente pour que les priorités soient utiles. Mais plus de tests sont nécessaires.*

Il y a UDPTransport.PRIORITY_LIMITS et UDPTransport.PRIORITY_WEIGHT (respectés par TimedWeightedPriorityMessageQueue), mais actuellement les poids sont presque tous égaux, donc il n'y a aucun effet. Cela pourrait être ajusté, bien sûr (mais comme vous le mentionnez, s'il n'y a pas de mise en file d'attente, cela n'a pas d'importance).

> *5) Le nouveau délai d'expiration maximal de 45s de la bibliothèque de streaming est probablement encore trop faible. La RFC TCP indique 60s. Il ne devrait probablement pas être plus court que le délai d'expiration maximal NTCP sous-jacent (vraisemblablement 60s).*

Ces 45s correspondent au timeout de retransmission maximal de la bibliothèque de streaming, pas au timeout du flux. TCP en pratique a des timeouts de retransmission d'ordres de grandeur inférieurs, bien qu'effectivement, cela puisse atteindre 60s sur des liens passant par des câbles exposés ou des transmissions satellite ;) Si nous augmentons le timeout de retransmission de la bibliothèque de streaming à par exemple 75 secondes, nous pourrions aller prendre une bière avant qu'une page web se charge (surtout en supposant un transport fiable à moins de 98%). C'est une des raisons pour lesquelles nous préférons NTCP.

### Réponse par zzz {#zzz-response}

Publié sur le nouveau Syndie, 2007-03-31

> *À 10 retransmissions, nous sommes déjà dans de beaux draps, je suis d'accord. Une, peut-être deux > retransmissions sont raisonnables, du point de vue de la couche transport, mais si l'autre côté est > trop congestionné pour acquitter à temps (même avec la capacité SACK/NACK implémentée), > nous ne pouvons pas faire grand-chose.* > > *À mon avis, pour vraiment traiter le problème fondamental, nous devons comprendre pourquoi le > router devient si congestionné qu'il n'arrive pas à acquitter à temps (ce qui, d'après ce que j'ai trouvé, est dû à > la contention CPU). Peut-être pouvons-nous jongler avec certaines choses dans le traitement du router pour > donner une priorité CPU plus élevée à la transmission d'un tunnel déjà existant qu'au déchiffrement d'une nouvelle requête de tunnel ? Bien que nous devions faire attention à éviter > la famine.*

Une de mes principales techniques de collecte de statistiques consiste à activer net.i2p.client.streaming.ConnectionPacketHandler=DEBUG et à observer les temps RTT et les tailles de fenêtre au fur et à mesure. Pour généraliser un peu, il est courant de voir 3 types de connexions : ~4s RTT, ~10s RTT, et ~30s RTT. L'objectif est d'essayer de réduire les connexions à 30s RTT. Si la contention CPU en est la cause, alors peut-être qu'un peu de jonglage suffira.

Réduire le max retrans SSU de 10 est vraiment juste un coup dans le noir car nous n'avons pas de bonnes données pour savoir si nous nous effondrons, si nous avons des problèmes TCP-over-TCP, ou quoi que ce soit d'autre, donc plus de données sont nécessaires.

> *Cela vaut la peine d'être étudié - que se passerait-il si nous désactivions simplement les retransmissions de SSU ? Cela conduirait probablement à des taux de renvoi beaucoup plus élevés de la bibliothèque de streaming, mais peut-être pas.*

Ce que je ne comprends pas, si vous pourriez développer, ce sont les avantages des retransmissions SSU pour le trafic non-streaming-lib. Avons-nous besoin que les messages de tunnel (par exemple) utilisent un transport semi-fiable ou peuvent-ils utiliser un transport non fiable ou plus ou moins fiable (1 ou 2 retransmissions maximum, par exemple) ? En d'autres termes, pourquoi la semi-fiabilité ?

> *(mais comme vous le mentionnez, s'il n'y a pas de file d'attente, cela n'a pas d'importance).*

J'ai implémenté l'envoi prioritaire pour UDP mais cela s'est déclenché environ 100 000 fois moins souvent que le code côté NTCP. C'est peut-être un indice pour une investigation plus poussée ou un indice - je ne comprends pas pourquoi il y aurait des embouteillages beaucoup plus fréquents avec NTCP, mais c'est peut-être un indice sur pourquoi NTCP performe moins bien.

### Question répondue par jrandom {#jrandom-followup}

Publié sur le nouveau Syndie, 31-03-2007

> *taux de retransmission SSU mesurés que nous avions observés avant l'implémentation de NTCP > (10-30+%)* > > Le router peut-il mesurer cela lui-même ? Si c'est le cas, un transport pourrait-il être sélectionné > en fonction des performances mesurées ? (c'est-à-dire si une connexion SSU vers un pair perd un > nombre déraisonnable de messages, privilégier NTCP lors de l'envoi vers ce pair)

Oui, il utilise actuellement cette statistique comme une détection MTU rudimentaire (si le taux de retransmission est élevé, il utilise la petite taille de paquet, mais s'il est faible, il utilise la grande taille de paquet). Nous avons essayé quelques approches lors de la première introduction de NTCP (et lors du premier abandon du transport TCP original) qui privilégieraient SSU mais feraient échouer ce transport facilement pour un pair, l'obligeant à se rabattre sur NTCP. Cependant, il y a certainement plus qui pourrait être fait à cet égard, bien que cela se complique rapidement (comment/quand ajuster/réinitialiser les enchères, s'il faut partager ces préférences entre plusieurs pairs ou non, s'il faut les partager entre plusieurs sessions avec le même pair (et pendant combien de temps), etc).

### Réponse de foofighter {#foofighter}

Publié sur le nouveau Syndie, 2007-03-26

Si j'ai bien compris, la raison principale en faveur de TCP (en général, tant l'ancienne que la nouvelle variété) était qu'on n'avait pas à se soucier de coder une bonne pile TCP. Ce qui n'est pas impossible à réussir... c'est juste que les piles TCP existantes ont 20 ans d'avance.

À ma connaissance, il n'y a pas eu beaucoup de théorie approfondie derrière la préférence de TCP par rapport à UDP, excepté les considérations suivantes :

- Un réseau TCP uniquement est très dépendant des pairs accessibles (ceux qui peuvent transmettre les connexions entrantes à travers leur NAT)
- Même si les pairs accessibles sont rares, le fait qu'ils aient une capacité élevée atténue quelque peu les problèmes de rareté topologique
- UDP permet le "NAT hole punching" qui permet aux gens d'être "en quelque sorte pseudo-accessibles" (avec l'aide d'introducers) alors qu'ils ne pourraient autrement que se connecter en sortie
- L'implémentation "ancienne" du transport TCP nécessitait beaucoup de threads, ce qui tuait les performances, tandis que le "nouveau" transport TCP fonctionne bien avec peu de threads
- Les routeurs de l'ensemble A plantent quand ils sont saturés d'UDP. Les routeurs de l'ensemble B plantent quand ils sont saturés de TCP.
- Il "semble" (c'est-à-dire qu'il y a quelques indications mais pas de données scientifiques ou de statistiques de qualité) que A soit plus largement déployé que B
- Certains réseaux transportent les datagrammes UDP non-DNS avec une qualité franchement minable, tout en se donnant encore la peine de transporter les flux TCP.

Dans ce contexte, une petite diversité de transports (autant que nécessaire, mais pas plus) semble sensée dans les deux cas. Lequel devrait être le transport principal dépend de leurs performances. J'ai vu des choses désagréables sur ma ligne quand j'ai essayé d'utiliser sa pleine capacité avec UDP. Des pertes de paquets de l'ordre de 35%.

Nous pourrions certainement essayer de jouer avec les priorités UDP versus TCP, mais je recommande la prudence à ce sujet. Je recommande vivement qu'elles ne soient pas modifiées trop radicalement d'un coup, car cela pourrait casser des choses.

### Réponse de zzz (à foofighter) {#zzz-foofighter}

Publié sur le nouveau Syndie, 27-03-2007

> *À ma connaissance, il n'y a pas eu beaucoup de théorie approfondie derrière la préférence de TCP par rapport à UDP, sauf les considérations suivantes :*

Ce sont tous des problèmes valides. Cependant, vous considérez les deux protocoles de manière isolée, plutôt que de réfléchir à quel protocole de transport est le mieux adapté pour un protocole de niveau supérieur particulier (c'est-à-dire avec ou sans bibliothèque de streaming).

Ce que je veux dire, c'est que vous devez prendre en compte la bibliothèque de streaming.

Donc soit modifier les préférences pour tout le monde, soit traiter différemment le trafic de la bibliothèque de streaming.

C'est de cela que parle ma proposition 1B) - avoir une préférence différente pour le trafic streaming-lib par rapport au trafic non streaming-lib (par exemple les messages de construction de tunnel).

> *Dans ce contexte, une petite diversité de transports (autant que nécessaire, mais > pas plus) semble sensée dans les deux cas. Lequel devrait être le transport principal > dépend de leurs performances respectives. J'ai vu des choses désagréables sur ma ligne quand j'ai > essayé d'utiliser sa pleine capacité avec UDP. Des pertes de paquets de l'ordre de 35%.*

D'accord. La nouvelle version .28 a peut-être amélioré les choses pour la perte de paquets sur UDP, ou peut-être pas.

Un point important - le code de transport se souvient effectivement des échecs d'un transport. Donc si UDP est le transport préféré, il l'essaiera en premier, mais s'il échoue pour une destination particulière, la tentative suivante pour cette destination essaiera NTCP plutôt que de réessayer UDP.

> *Nous pourrions certainement essayer de jouer avec les priorités UDP versus TCP, mais j'encouragerais > la prudence à ce sujet. J'encouragerais à ce qu'elles ne soient pas changées trop radicalement d'un > coup, ou cela pourrait casser des choses.*

Nous avons quatre boutons de réglage - les quatre valeurs d'enchère (SSU et NTCP, pour déjà-connecté et pas-encore-connecté). Nous pourrions faire en sorte que SSU soit préféré à NTCP seulement si les deux sont connectés, par exemple, mais essayer NTCP en premier si aucun transport n'est connecté.

L'autre façon de le faire progressivement est de ne déplacer que le trafic de la bibliothèque de streaming (la proposition 1B), cependant cela pourrait être difficile et pourrait avoir des implications d'anonymat, je ne sais pas. Ou peut-être déplacer le trafic seulement pour le premier saut sortant (c'est-à-dire ne pas propager le flag vers le router suivant), ce qui ne vous donne qu'un bénéfice partiel mais pourrait être plus anonyme et plus facile.

## Résultats de la Discussion {#results}

... et autres changements connexes dans la même période (2007) :

- Un réglage significatif des paramètres de la bibliothèque de streaming,
  augmentant considérablement les performances sortantes, a été implémenté dans la version 0.6.1.28
- L'envoi prioritaire pour NTCP a été implémenté dans la version 0.6.1.28
- L'envoi prioritaire pour SSU a été implémenté par zzz mais n'a jamais été intégré
- Le contrôle avancé des offres de transport
  i2np.udp.preferred a été implémenté dans la version 0.6.1.29.
- Le pushback pour NTCP a été implémenté dans la version 0.6.1.30, désactivé dans la version 0.6.1.31 en raison de préoccupations d'anonymat,
  et réactivé avec des améliorations pour répondre à ces préoccupations dans la version 0.6.1.32.
- Aucune des propositions 1-5 de zzz n'a été implémentée.
