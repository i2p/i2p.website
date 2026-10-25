---
title: "Secure Semireliable UDP (SSU)"
description: "Transport UDP original utilisé avant SSU2 (obsolète)"
slug: "ssu-overview"
aliases:
  - "/fr/udp"
  - "/fr/udp/"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
---

**DÉPRÉCIÉ** - SSU a été remplacé par SSU2. Le support SSU a été supprimé d'i2pd dans la version 2.44.0 (API 0.9.56) novembre 2022. Le support SSU a été supprimé de Java I2P dans la version 2.4.0 (API 0.9.61) décembre 2023.

SSU (également appelé "UDP" dans une grande partie de la documentation I2P et des interfaces utilisateur) était l'un des deux [transports](/docs/transport) implémentés dans I2P. L'autre est [NTCP2](/docs/specs/ntcp2). Le support pour [NTCP](/docs/legacy/ntcp) a été supprimé.

SSU a été introduit dans la version 0.6 d'I2P. Dans une installation I2P standard, le router utilise à la fois NTCP et SSU pour les connexions sortantes. SSU-over-IPv6 est pris en charge depuis la version 0.9.8.

SSU est qualifié de "semi-fiable" car il retransmettra de manière répétée les messages non accusés réception, mais seulement jusqu'à un nombre maximum de fois. Après cela, le message est abandonné.

## Services SSU

Comme le transport NTCP, SSU fournit un transport de données fiable, chiffré, orienté connexion et point-à-point. Propre à SSU, il fournit également des services de détection IP et de traversée NAT, notamment :

- Traversée coopérative de NAT/pare-feu utilisant les [introducers](#introduction)
- Détection d'IP locale par inspection des paquets entrants et [peer testing](#peerTesting)
- Communication du statut du pare-feu et de l'IP locale, et des changements de l'un ou l'autre vers NTCP
- Communication du statut du pare-feu et de l'IP locale, et des changements de l'un ou l'autre, vers le router et l'interface utilisateur

## Spécification d'adresse du router {#ra}

Les propriétés suivantes sont stockées dans la base de données réseau.

- **Transport name:** SSU
- **caps:** [B,C,4,6] [Voir ci-dessous](#capabilities).
- **host:** IP (IPv4 ou IPv6).
  L'adresse IPv6 raccourcie (avec "::") est autorisée.
  Peut être présent ou non si derrière un pare-feu.
  Les noms d'hôte étaient précédemment autorisés, mais sont dépréciés depuis la version 0.9.32. Voir la proposition 141.
- **iexp[0-2]:** Expiration de cet introducer.
  Chiffres ASCII, en secondes depuis l'époque.
  Présent uniquement si derrière un pare-feu, et que des introducers sont requis.
  Optionnel (même si d'autres propriétés pour cet introducer sont présentes).
  Depuis la version 0.9.30, proposition 133.
- **ihost[0-2]:** IP de l'introducer (IPv4 ou IPv6).
  Les noms d'hôte étaient précédemment autorisés, mais sont dépréciés depuis la version 0.9.32. Voir la proposition 141.
  L'adresse IPv6 raccourcie (avec "::") est autorisée.
  Présent uniquement si derrière un pare-feu, et que des introducers sont requis.
  [Voir ci-dessous](#introduction).
- **ikey[0-2]:** Clé d'introduction Base 64 de l'introducer. [Voir ci-dessous](#key).
  Présent uniquement si derrière un pare-feu, et que des introducers sont requis.
  [Voir ci-dessous](#introduction).
- **iport[0-2]:** Port de l'introducer 1024 - 65535.
  Présent uniquement si derrière un pare-feu, et que des introducers sont requis.
  [Voir ci-dessous](#introduction).
- **itag[0-2]:** Tag de l'introducer 1 - (2^32 - 1)
  Chiffres ASCII.
  Présent uniquement si derrière un pare-feu, et que des introducers sont requis.
  [Voir ci-dessous](#introduction).
- **key:** Clé d'introduction Base 64. [Voir ci-dessous](#key).
- **mtu:** Optionnel. Par défaut et max est 1484. Min est 620.
  Doit être présent pour IPv6, où le min est 1280 et le max est 1488
  (le max était 1472 avant la version 0.9.28).
  Le MTU IPv6 doit être un multiple de 16.
  (MTU IPv4 + 4) doit être un multiple de 16.
  [Voir ci-dessous](#mtu).
- **port:** 1024 - 65535
  Peut être présent ou non si derrière un pare-feu.

# Détails du protocole

## Contrôle de congestion {#congestioncontrol}

Le besoin de SSU d'une livraison seulement semi-fiable, d'un fonctionnement compatible TCP et de la capacité d'un débit élevé permet une grande latitude dans le contrôle de congestion. L'algorithme de contrôle de congestion décrit ci-dessous est conçu pour être à la fois efficace en bande passante et simple à implémenter.

Les paquets sont programmés selon la politique du router, en prenant soin de ne pas dépasser la capacité sortante du router ou de dépasser la capacité mesurée du pair distant. La capacité mesurée fonctionne selon les principes du démarrage lent et de l'évitement de congestion de TCP, avec des augmentations additives de la capacité d'envoi et des diminutions multiplicatives face à la congestion. Contrairement à TCP, les routers peuvent abandonner certains messages après une période donnée ou un nombre de retransmissions tout en continuant à transmettre d'autres messages.

Les techniques de détection de congestion diffèrent également de TCP, puisque chaque message a son propre identifiant unique et non séquentiel, et chaque message a une taille limitée - au maximum 32 Ko. Pour transmettre efficacement ce retour d'information à l'expéditeur, le récepteur inclut périodiquement une liste des identifiants de messages entièrement acquittés et peut également inclure des champs de bits pour les messages partiellement reçus, où chaque bit représente la réception d'un fragment. Si des fragments dupliqués arrivent, le message doit être acquitté à nouveau, ou si le message n'a toujours pas été entièrement reçu, le champ de bits doit être retransmis avec toutes les nouvelles mises à jour.

L'implémentation actuelle ne remplit pas les paquets à une taille particulière, mais place simplement un fragment de message unique dans un paquet et l'envoie (en veillant à ne pas dépasser le MTU).

### MTU {#mtu}

À partir de la version 0.8.12 du router, deux valeurs MTU sont utilisées pour IPv4 : 620 et 1484. La valeur MTU est ajustée en fonction du pourcentage de paquets qui sont retransmis.

Pour les deux valeurs de MTU, il est souhaitable que (MTU % 16) == 12, afin que la partie payload après l'en-tête IP/UDP de 28 octets soit un multiple de 16 octets, à des fins de chiffrement.

Pour la petite valeur MTU, il est souhaitable d'emballer efficacement un message Variable Tunnel Build de 2646 octets dans plusieurs paquets ; avec un MTU de 620 octets, il s'intègre parfaitement dans 5 paquets.

D'après les mesures, 1492 convient à presque tous les messages I2NP de taille raisonnablement petite (les messages I2NP plus volumineux peuvent atteindre 1900 à 4500 octets, ce qui ne rentrera de toute façon pas dans un MTU de réseau actif).

Les valeurs MTU étaient de 608 et 1492 pour les versions 0.8.9 - 0.8.11. La grande MTU était de 1350 avant la version 0.8.9.

La taille maximale des paquets reçus est de 1571 octets depuis la version 0.8.12. Pour les versions 0.8.9 à 0.8.11, elle était de 1535 octets. Avant la version 0.8.9, elle était de 2048 octets.

Depuis la version 0.9.2, si le MTU de l'interface réseau d'un router est inférieur à 1484, il publiera cette information dans la base de données réseau, et les autres routers devraient respecter cette valeur lors de l'établissement d'une connexion.

Pour IPv6, la MTU minimale est de 1280. L'en-tête IPv6 IP/UDP fait 48 octets, nous utilisons donc une MTU où (MTU % 16 == 0), ce qui est vrai pour 1280. La MTU IPv6 maximale est de 1488. (le maximum était de 1472 avant la version 0.9.28).

### Limites de taille des messages {#max}

Bien que la taille maximale des messages soit nominalement de 32 Ko, la limite pratique diffère. Le protocole limite le nombre de fragments à 7 bits, soit 128. L'implémentation actuelle, cependant, limite chaque message à un maximum de 64 fragments, ce qui est suffisant pour 64 * 534 = 33,3 Ko lors de l'utilisation du MTU 608. En raison de la surcharge pour les leaseSets groupés et les clés de session, la limite pratique au niveau de l'application est d'environ 6 Ko inférieure, soit environ 26 Ko. Des travaux supplémentaires sont nécessaires pour élever la limite de transport UDP au-dessus de 32 Ko. Pour les connexions utilisant le MTU plus grand, des messages plus volumineux sont possibles.

## Délai d'expiration d'inactivité

Le délai d'expiration d'inactivité et la fermeture de connexion sont à la discrétion de chaque point de terminaison et peuvent varier. L'implémentation actuelle réduit le délai d'expiration lorsque le nombre de connexions approche du maximum configuré, et augmente le délai d'expiration lorsque le nombre de connexions est faible. Le délai d'expiration minimum recommandé est de deux minutes ou plus, et le délai d'expiration maximum recommandé est de dix minutes ou plus.

## Clés {#keys}

Tout le chiffrement utilisé est AES256/CBC avec des clés de 32 octets et des IV de 16 octets. Lorsqu'Alice initie une session avec Bob, les clés MAC et de session sont négociées dans le cadre de l'échange DH, puis utilisées respectivement pour le HMAC et le chiffrement. Pendant l'échange DH, l'introKey publiquement connaissable de Bob est utilisée pour le MAC et le chiffrement.

Le message initial et la réponse subséquente utilisent tous deux l'introKey du répondeur (Bob) - le répondeur n'a pas besoin de connaître l'introKey du demandeur (Alice). La clé de signature DSA utilisée par Bob devrait déjà être connue d'Alice lorsqu'elle le contacte, bien que la clé DSA d'Alice puisse ne pas encore être connue de Bob.

Lors de la réception d'un message, le récepteur vérifie l'adresse IP et le port "from" avec toutes les sessions établies - s'il y a des correspondances, les clés MAC de cette session sont testées dans le HMAC. Si aucune d'entre elles ne se vérifie ou s'il n'y a pas d'adresses IP correspondantes, le récepteur essaie sa introKey dans le MAC. Si cela ne se vérifie pas, le paquet est abandonné. Si cela se vérifie, il est interprété selon le type de message, bien que si le récepteur est surchargé, il puisse être abandonné de toute façon.

Si Alice et Bob ont une session établie, mais qu'Alice perd les clés pour une raison quelconque et qu'elle souhaite contacter Bob, elle peut à tout moment simplement établir une nouvelle session via le SessionRequest et les messages associés. Si Bob a perdu la clé mais qu'Alice ne le sait pas, elle tentera d'abord de l'inciter à répondre, en envoyant un DataMessage avec le flag wantReply activé, et si Bob échoue continuellement à répondre, elle supposera que la clé est perdue et en rétablira une nouvelle.

Pour l'accord de clé DH, le groupe MODP 2048 bits (#14) de [RFC3526](http://www.faqs.org/rfcs/rfc3526.html) est utilisé :

```
  p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
  g = 2
```
Ce sont les mêmes p et g utilisés pour le [chiffrement ElGamal](/docs/specs/cryptography#elgamal) d'I2P.

## Prévention de la Relecture {#replay}

La prévention de la relecture au niveau de la couche SSU se produit en rejetant les paquets avec des horodatages excessivement anciens ou ceux qui réutilisent un IV. Pour détecter les IV dupliqués, une séquence de filtres de Bloom est utilisée pour "se dégrader" périodiquement afin que seuls les IV récemment ajoutés soient détectés.

Les messageIds utilisés dans les DataMessages sont définis dans les couches au-dessus du transport SSU et sont transmis de manière transparente. Ces IDs ne suivent aucun ordre particulier - en fait, ils sont probablement entièrement aléatoires. La couche SSU ne fait aucune tentative de prévention de la rejeu des messageId - les couches supérieures doivent en tenir compte.

## Adressage {#addressing}

Pour contacter un pair SSU, l'un des deux ensembles d'informations suivants est nécessaire : une adresse directe, lorsque le pair est accessible publiquement, ou une adresse indirecte, pour utiliser un tiers afin d'introduire le pair. Il n'y a aucune restriction sur le nombre d'adresses qu'un pair peut avoir.

```
    Direct: host, port, introKey, options
  Indirect: tag, relayhost, port, relayIntroKey, targetIntroKey, options
```
Chacune des adresses peut également exposer une série d'options - des capacités spéciales de ce pair particulier. Pour une liste des capacités disponibles, voir [ci-dessous](#capabilities).

Les adresses, options et capacités sont publiées dans la [base de données réseau](/docs/overview/network-database).

## Établissement de Session Directe {#direct}

L'établissement de session direct est utilisé lorsqu'aucune tierce partie n'est requise pour le traversal NAT. La séquence de messages est la suivante :

### Établissement de connexion (Direct) {#establishDirect}

Alice se connecte directement à Bob. IPv6 est supporté à partir de la version 0.9.8.

```
        Alice                         Bob
    SessionRequest --------------------->
          <--------------------- SessionCreated
    SessionConfirmed ------------------->
          <--------------------- DeliveryStatusMessage
          <--------------------- DatabaseStoreMessage
    DatabaseStoreMessage --------------->
    Data <--------------------------> Data
```
Après réception du message SessionConfirmed, Bob envoie un petit [message DeliveryStatus](/docs/specs/i2np#msg_DeliveryStatus) comme confirmation. Dans ce message, l'ID de message de 4 octets est défini sur un nombre aléatoire, et le "temps d'arrivée" de 8 octets est défini sur l'ID réseau actuel, qui est 2 (c'est-à-dire 0x0000000000000002).

Après l'envoi du message de statut, les pairs échangent généralement des [messages DatabaseStore](/docs/specs/i2np#msg_DatabaseStore) contenant leurs [RouterInfos](/docs/specs/common-structures#struct_RouterInfo), cependant, cela n'est pas obligatoire.

Il ne semble pas que le type du message de statut ou son contenu ait de l'importance. Il avait été ajouté à l'origine parce que le message DatabaseStore était retardé de plusieurs secondes ; puisque le store est maintenant envoyé immédiatement, peut-être que le message de statut peut être supprimé.

## Introduction {#introduction}

Les clés d'introduction sont délivrées via un canal externe (la base de données réseau), où elles ont traditionnellement été identiques au Hash du router jusqu'à la version 0.9.47, mais peuvent être aléatoires à partir de la version 0.9.48. Elles doivent être utilisées lors de l'établissement d'une clé de session. Pour l'adresse indirecte, le pair doit d'abord contacter l'hôte relais et lui demander une introduction au pair connu à cet hôte relais sous l'étiquette donnée. Si possible, l'hôte relais envoie un message au pair adressé lui disant de contacter le pair demandeur, et donne également au pair demandeur l'IP et le port sur lesquels le pair adressé se trouve. De plus, le pair qui établit la connexion doit déjà connaître les clés publiques du pair auquel il se connecte (mais pas nécessairement celles d'un pair relais intermédiaire).

L'établissement de session indirect au moyen d'une introduction par une tierce partie est nécessaire pour une traversée NAT efficace. Charlie, un router derrière un NAT ou pare-feu qui n'autorise pas les paquets UDP entrants non sollicités, contacte d'abord quelques pairs, en choisissant certains pour servir d'introducteurs. Chacun de ces pairs (Bob, Bill, Betty, etc.) fournit à Charlie une étiquette d'introduction - un nombre aléatoire de 4 octets - qu'il rend ensuite disponible au public comme méthodes pour le contacter. Alice, un router qui dispose des méthodes de contact publiées de Charlie, envoie d'abord un paquet RelayRequest à un ou plusieurs des introducteurs, demandant à chacun de la présenter à Charlie (en offrant l'étiquette d'introduction pour identifier Charlie). Bob transmet alors un paquet RelayIntro à Charlie incluant l'adresse IP publique et le numéro de port d'Alice, puis renvoie à Alice un paquet RelayResponse contenant l'adresse IP publique et le numéro de port de Charlie. Quand Charlie reçoit le paquet RelayIntro, il envoie un petit paquet aléatoire vers l'IP et le port d'Alice (perçant un trou dans son NAT/pare-feu), et quand Alice reçoit le paquet RelayResponse de Bob, elle commence un nouvel établissement de session bidirectionnel complet avec l'IP et le port spécifiés.

### Établissement de Connexion (Indirect Utilisant un Introducer) {#establishIndirect}

Alice se connecte d'abord à l'introducer Bob, qui relaie la demande à Charlie.

```
        Alice                         Bob                  Charlie
    RelayRequest ---------------------->
         <-------------- RelayResponse    RelayIntro ----------->
         <-------------------------------------------- HolePunch (data ignored)
    SessionRequest -------------------------------------------->
         <-------------------------------------------- SessionCreated
    SessionConfirmed ------------------------------------------>
         <-------------------------------------------- DeliveryStatusMessage
         <-------------------------------------------- DatabaseStoreMessage
    DatabaseStoreMessage -------------------------------------->
    Data <--------------------------------------------------> Data
```
Après le perçage de NAT, la session est établie entre Alice et Charlie comme dans un établissement direct.

### Notes IPv6

IPv6 est pris en charge à partir de la version 0.9.8. Les adresses de relais publiées peuvent être IPv4 ou IPv6, et la communication Alice-Bob peut se faire via IPv4 ou IPv6. Jusqu'à la version 0.9.49, la communication Bob-Charlie et Alice-Charlie se fait uniquement via IPv4. Le relais pour IPv6 est pris en charge à partir de la version 0.9.50. Voir la spécification pour plus de détails.

Bien que la spécification ait été modifiée à partir de la version 0.9.8, la communication Alice-Bob via IPv6 n'a pas été réellement prise en charge avant la version 0.9.50. Les versions antérieures des routers Java publiaient par erreur la capacité 'C' pour les adresses IPv6, même si elles n'agissaient pas réellement comme un introducer via IPv6. Par conséquent, les routers ne devraient faire confiance à la capacité 'C' sur une adresse IPv6 que si la version du router est 0.9.50 ou supérieure.

## Test de pairs {#peerTesting}

L'automatisation des tests de joignabilité collaboratifs pour les pairs est rendue possible par une séquence de messages PeerTest. Avec son exécution appropriée, un pair sera capable de déterminer sa propre joignabilité et pourra mettre à jour son comportement en conséquence. Le processus de test est assez simple :

```
        Alice                  Bob                  Charlie
    PeerTest ------------------->
                             PeerTest-------------------->
                                <-------------------PeerTest
         <-------------------PeerTest
         <------------------------------------------PeerTest
    PeerTest------------------------------------------>
         <------------------------------------------PeerTest
```
Chacun des messages PeerTest transporte un nonce identifiant la série de tests elle-même, tel qu'initialisé par Alice. Si Alice ne reçoit pas un message particulier qu'elle attend, elle retransmettra en conséquence, et en fonction des données reçues ou des messages manquants, elle connaîtra son accessibilité. Les différents états finaux qui peuvent être atteints sont les suivants :

- Si elle ne reçoit pas de réponse de Bob, elle retransmettra jusqu'à un certain nombre de fois, mais si aucune réponse n'arrive jamais, elle saura que son firewall ou NAT est mal configuré d'une manière ou d'une autre, rejetant tous les paquets UDP entrants même en réponse directe à un paquet sortant. Alternativement, Bob peut être hors service ou incapable d'obtenir une réponse de Charlie.

- Si Alice ne reçoit pas de message PeerTest avec le
  nonce attendu d'une tierce partie (Charlie), elle retransmettra
  sa requête initiale à Bob jusqu'à un certain nombre de fois, même
  si elle a déjà reçu la réponse de Bob. Si le premier message de Charlie
  ne passe toujours pas mais que celui de Bob passe, elle sait qu'elle est
  derrière un NAT ou un pare-feu qui rejette les tentatives de connexion
  non sollicitées et que la redirection de port ne fonctionne pas correctement (l'IP
  et le port que Bob a fournis devraient être redirigés).

- Si Alice reçoit le message PeerTest de Bob et les deux messages PeerTest de Charlie, mais que les numéros d'IP et de port contenus dans les seconds messages de Bob et Charlie ne correspondent pas, elle sait qu'elle se trouve derrière un NAT symétrique, qui réécrit tous ses paquets sortants avec des ports « from » différents pour chaque pair contacté. Elle devra explicitement transférer un port et toujours garder ce port exposé pour la connectivité distante, en ignorant toute découverte de port ultérieure.

- Si Alice reçoit le premier message de Charlie mais pas le second,
  elle retransmettra son message PeerTest à Charlie jusqu'à un
  certain nombre de fois, mais si aucune réponse n'est reçue, elle sait
  que Charlie est soit confus, soit n'est plus en ligne.

Alice devrait choisir Bob de manière arbitraire parmi les pairs connus qui semblent capables de participer aux tests de pairs. Bob à son tour devrait choisir Charlie de manière arbitraire parmi les pairs qu'il connaît et qui semblent capables de participer aux tests de pairs et qui sont sur une IP différente de celle de Bob et Alice. Si la première condition d'erreur se produit (Alice ne reçoit pas de messages PeerTest de Bob), Alice peut décider de désigner un nouveau pair comme Bob et réessayer avec un nonce différent.

La clé d'introduction d'Alice est incluse dans tous les messages PeerTest afin que Charlie puisse la contacter sans connaître d'informations supplémentaires. Depuis la version 0.9.15, Alice doit avoir une session établie avec Bob, pour prévenir les attaques de spoofing. Alice ne doit pas avoir de session établie avec Charlie pour que le test de pair soit valide. Alice peut ensuite établir une session avec Charlie, mais ce n'est pas obligatoire.

### Notes IPv6

Jusqu'à la version 0.9.26, seuls les tests d'adresses IPv4 sont pris en charge. Seuls les tests d'adresses IPv4 sont pris en charge. Par conséquent, toute communication Alice-Bob et Alice-Charlie doit passer par IPv4. La communication Bob-Charlie, cependant, peut passer par IPv4 ou IPv6. L'adresse d'Alice, lorsqu'elle est spécifiée dans le message PeerTest, doit faire 4 octets. À partir de la version 0.9.27, les tests d'adresses IPv6 sont pris en charge, et la communication Alice-Bob et Alice-Charlie peut passer par IPv6, si Bob et Charlie indiquent leur support avec une capacité 'B' dans leur adresse IPv6 publiée. Voir la [Proposition 126](/spec/proposals/126-ipv6-peer-testing) pour plus de détails.

Avant la version 0.9.50, Alice envoie la requête à Bob en utilisant une session existante via le transport (IPv4 ou IPv6) qu'elle souhaite tester. Quand Bob reçoit une requête d'Alice via IPv4, Bob doit sélectionner un Charlie qui annonce une adresse IPv4. Quand Bob reçoit une requête d'Alice via IPv6, Bob doit sélectionner un Charlie qui annonce une adresse IPv6. La communication réelle entre Bob et Charlie peut se faire via IPv4 ou IPv6 (c'est-à-dire, indépendamment du type d'adresse d'Alice).

Depuis la version 0.9.50, si le message est envoyé via IPv6 pour un test de pair IPv4, ou (depuis la version 0.9.50) via IPv4 pour un test de pair IPv6, Alice doit inclure son adresse d'introduction et son port.

Voir [Proposition 158](/spec/proposals/158) pour plus de détails.

## Fenêtre de transmission, ACKs et retransmissions {#acks}

Le message DATA peut contenir des ACK de messages complets et des ACK partiels de fragments individuels d'un message. Voir la section sur les messages de données de [la page de spécification du protocole](/docs/legacy/ssu) pour plus de détails.

Les détails des stratégies de fenêtrage, d'ACK et de retransmission ne sont pas spécifiés ici. Voir le code Java pour l'implémentation actuelle. Pendant la phase d'établissement et pour les tests de pairs, les routers doivent implémenter un backoff exponentiel pour la retransmission. Pour une connexion établie, les routers doivent implémenter une fenêtre de transmission ajustable, une estimation RTT et un timeout, similaire à TCP ou [streaming](/docs/api/streaming). Voir le code pour les paramètres initiaux, minimum et maximum.

## Sécurité {#security}

Les adresses sources UDP peuvent, bien sûr, être usurpées. De plus, les adresses IP et les ports contenus dans des messages SSU spécifiques (RelayRequest, RelayResponse, RelayIntro, PeerTest) peuvent ne pas être légitimes. En outre, certaines actions et réponses peuvent nécessiter une limitation de débit.

Les détails de la validation ne sont pas spécifiés ici. Les implémenteurs devraient ajouter des défenses là où c'est approprié.

## Capacités des Pairs {#capabilities}

Une ou plusieurs capacités peuvent être publiées dans l'option "caps". Les capacités peuvent être dans n'importe quel ordre, mais "BC46" est l'ordre recommandé, pour assurer la cohérence entre les implémentations.

**B** : Si l'adresse du pair contient la capacité 'B', cela signifie qu'il est disposé et capable de participer aux tests de pairs en tant que 'Bob' ou 'Charlie'. Jusqu'à la version 0.9.26, les tests de pairs n'étaient pas pris en charge pour les adresses IPv6, et la capacité 'B', si présente pour une adresse IPv6, devait être ignorée. À partir de la version 0.9.27, les tests de pairs sont pris en charge pour les adresses IPv6, et la présence ou l'absence de la capacité 'B' dans une adresse IPv6 indique le support réel (ou l'absence de support).

**C** : Si l'adresse du pair contient la capacité 'C', cela signifie qu'il est disposé et capable de servir d'introducer via cette adresse - servant d'introducer Bob pour un Charlie autrement inaccessible. Avant la version 0.9.50, les routers Java publiaient incorrectement la capacité 'C' pour les adresses IPv6, même si les introducers IPv6 n'étaient pas entièrement implémentés. Par conséquent, les routers doivent supposer que les versions antérieures à 0.9.50 ne peuvent pas agir comme introducer sur IPv6, même si la capacité 'C' est annoncée.

**4** : À partir de la version 0.9.50, indique la capacité IPv4 sortante. Si une IP est publiée dans le champ host, cette capacité n'est pas nécessaire. S'il s'agit d'une adresse avec des introducers pour les introductions IPv4, '4' devrait être inclus. Si le router est caché, '4' et '6' peuvent être combinés dans une seule adresse.

**6** : À partir de la version 0.9.50, indique la capacité IPv6 sortante. Si une IP est publiée dans le champ host, cette capacité n'est pas nécessaire. Si c'est une adresse avec des introducers pour les introductions IPv6, '6' devrait être inclus (non supporté actuellement). Si le router est caché, '4' et '6' peuvent être combinés dans une seule adresse.

# Travaux futurs {#future}

Note : Ces problèmes seront traités lors du développement de SSU2.

- L'analyse de la performance actuelle de SSU, incluant l'évaluation de l'ajustement de la taille de fenêtre et d'autres paramètres, ainsi que l'ajustement de l'implémentation du protocole pour améliorer les performances, est un sujet pour des travaux futurs.

- L'implémentation actuelle envoie de manière répétée des accusés de réception pour les mêmes paquets,
  ce qui augmente inutilement la surcharge.

- La valeur MTU petite par défaut de 620 devrait être analysée et possiblement augmentée.
  La stratégie actuelle d'ajustement MTU devrait être évaluée.
  Est-ce qu'un paquet de streaming lib de 1730 octets rentre dans 3 petits paquets SSU ? Probablement pas.

- Le protocole devrait être étendu pour échanger les MTU pendant la configuration.

- La regénération de clés n'est actuellement pas implémentée et ne le sera jamais.

- L'utilisation potentielle des champs 'challenge' dans RelayIntro et RelayResponse,
  et l'utilisation du champ de remplissage dans SessionRequest et SessionCreated, n'est pas documentée.

- Un ensemble de tailles de paquets fixes pourrait être approprié pour masquer davantage la fragmentation des données aux adversaires externes, mais le remplissage au niveau du tunnel, garlic et de bout en bout devrait être suffisant pour la plupart des besoins d'ici là.

- Les heures de connexion dans SessionCreated et SessionConfirmed semblent être inutilisées ou non vérifiées.

# Spécification {#spec}

[Maintenant sur la page de spécification SSU](/docs/legacy/ssu).
