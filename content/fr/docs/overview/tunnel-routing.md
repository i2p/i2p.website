---
title: "Routage de tunnel"
description: "Aperçu de la terminologie, de la construction et du fonctionnement des tunnels I2P"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## Aperçu

Cette page contient un aperçu de la terminologie et du fonctionnement des tunnels I2P, avec des liens vers des pages plus techniques, des détails et des spécifications.

Comme expliqué brièvement dans l'[introduction](/docs/overview/intro/), I2P construit des "tunnels" virtuels - des chemins temporaires et unidirectionnels à travers une séquence de routers. Ces tunnels sont classés soit comme tunnels entrants (où tout ce qui leur est donné va vers le créateur du tunnel) soit comme tunnels sortants (où le créateur du tunnel pousse les messages loin de lui). Quand Alice veut envoyer un message à Bob, elle l'enverra (typiquement) par l'un de ses tunnels sortants existants avec des instructions pour que l'endpoint de ce tunnel le transmette au router passerelle pour l'un des tunnels entrants actuels de Bob, qui à son tour le passe à Bob.

![Alice se connectant via son tunnel sortant à Bob via son tunnel entrant](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Vocabulaire des tunnels

- **Tunnel gateway** - le premier router dans un tunnel. Pour les tunnels entrants, c'est celui mentionné dans le LeaseSet publié dans la [base de données réseau](/docs/overview/network-database/). Pour les tunnels sortants, le gateway est le router d'origine. (par exemple, A et D ci-dessus)

- **Point de terminaison de tunnel** - le dernier router dans un tunnel. (par exemple, C et F ci-dessus)

- **Participant de tunnel** - tous les routeurs dans un tunnel à l'exception de la passerelle ou du point de terminaison (par exemple, B et E ci-dessus)

- **tunnel n-Hop** - un tunnel avec un nombre spécifique de sauts inter-routeurs, par exemple :
  - **tunnel 0-hop** - un tunnel où la passerelle est aussi le point de terminaison
  - **tunnel 1-hop** - un tunnel où la passerelle communique directement avec le point de terminaison
  - **tunnel 2-(ou plus)-hop** - un tunnel où il y a au moins un participant tunnel intermédiaire. (le diagramme ci-dessus inclut deux tunnels 2-hop - un sortant d'Alice, un entrant vers Bob)

- **Tunnel ID** - Un [entier de 4 octets](/docs/specs/common-structures/#type_TunnelId) différent pour chaque saut dans un tunnel, et unique parmi tous les tunnels sur un router. Choisi aléatoirement par le créateur du tunnel.

---

## Informations de Construction de Tunnel

Les routers qui remplissent les trois rôles (passerelle, participant, point terminal) reçoivent différents éléments de données dans le [Message de Construction de Tunnel](/docs/specs/tunnel-creation/) initial pour accomplir leurs tâches :

**Le tunnel gateway reçoit :**

- **clé de chiffrement tunnel** - une [clé privée AES](/docs/specs/common-structures/#type_SessionKey) pour chiffrer les messages et instructions vers le prochain saut
- **clé IV tunnel** - une [clé privée AES](/docs/specs/common-structures/#type_SessionKey) pour double-chiffrer l'IV vers le prochain saut
- **clé de réponse** - une [clé publique AES](/docs/specs/common-structures/#type_SessionKey) pour chiffrer la réponse à la demande de construction du tunnel
- **IV de réponse** - l'IV pour chiffrer la réponse à la demande de construction du tunnel
- **id tunnel** - entier de 4 octets (passerelles entrantes uniquement)
- **prochain saut** - quel router est le suivant dans le chemin (sauf s'il s'agit d'un tunnel à 0 saut, et que la passerelle est aussi le point de terminaison)
- **id tunnel suivant** - L'ID du tunnel sur le prochain saut

**Tous les participants intermédiaires du tunnel reçoivent :**

- **clé de chiffrement de tunnel** - une [clé privée AES](/docs/specs/common-structures/#type_SessionKey) pour chiffrer les messages et instructions vers le prochain saut
- **clé IV de tunnel** - une [clé privée AES](/docs/specs/common-structures/#type_SessionKey) pour double-chiffrer l'IV vers le prochain saut
- **clé de réponse** - une [clé publique AES](/docs/specs/common-structures/#type_SessionKey) pour chiffrer la réponse à la demande de construction de tunnel
- **IV de réponse** - l'IV pour chiffrer la réponse à la demande de construction de tunnel
- **ID de tunnel** - entier de 4 octets
- **prochain saut** - quel router est le suivant dans le chemin
- **ID de tunnel suivant** - L'ID de tunnel sur le prochain saut

**Le point de terminaison du tunnel reçoit :**

- **clé de chiffrement de tunnel** - une [clé privée AES](/docs/specs/common-structures/#type_SessionKey) pour chiffrer les messages et instructions vers le point de terminaison (lui-même)
- **clé IV de tunnel** - une [clé privée AES](/docs/specs/common-structures/#type_SessionKey) pour double-chiffrer l'IV vers le point de terminaison (lui-même)
- **clé de réponse** - une [clé publique AES](/docs/specs/common-structures/#type_SessionKey) pour chiffrer la réponse à la demande de construction de tunnel (points de terminaison sortants uniquement)
- **IV de réponse** - l'IV pour chiffrer la réponse à la demande de construction de tunnel (points de terminaison sortants uniquement)
- **ID de tunnel** - entier de 4 octets (points de terminaison sortants uniquement)
- **routeur de réponse** - la passerelle d'entrée du tunnel par laquelle envoyer la réponse (points de terminaison sortants uniquement)
- **ID de tunnel de réponse** - L'ID de tunnel du routeur de réponse (points de terminaison sortants uniquement)

Les détails se trouvent dans la [spécification de création de tunnel](/docs/specs/tunnel-creation/).

---

## Mise en commun des tunnels

Plusieurs tunnels pour un objectif particulier peuvent être regroupés dans un "pool de tunnels", comme décrit dans la [spécification des tunnels](/docs/specs/tunnel-implementation/#tunnel.pooling). Ceci fournit de la redondance et de la bande passante supplémentaire. Les pools utilisés par le router lui-même sont appelés "tunnels exploratoires". Les pools utilisés par les applications sont appelés "tunnels clients".

---

## Longueur du tunnel

Comme mentionné ci-dessus, chaque client demande à son router de fournir des tunnels incluant au moins un certain nombre de sauts. La décision concernant le nombre de routers à avoir dans ses tunnels sortants et entrants a un effet important sur la latence, le débit, la fiabilité et l'anonymat fournis par I2P - plus les messages doivent passer par de pairs, plus il faut de temps pour arriver à destination et plus il est probable qu'un de ces routers échoue prématurément. Moins il y a de routers dans un tunnel, plus il est facile pour un adversaire de monter des attaques d'analyse de trafic et de percer l'anonymat de quelqu'un. Les longueurs de tunnel sont spécifiées par les clients via les [options I2CP](/docs/specs/i2cp/#options). Le nombre maximum de sauts dans un tunnel est de 7.

### tunnels à 0 saut

Sans router distant dans un tunnel, l'utilisateur bénéficie d'un déni plausible très basique (puisque personne ne sait avec certitude que le pair qui lui a envoyé le message ne faisait pas simplement que le transmettre dans le cadre du tunnel). Cependant, il serait assez facile de monter une attaque d'analyse statistique et de remarquer que les messages ciblant une destination spécifique sont toujours envoyés via une seule passerelle. L'analyse statistique contre les tunnels sortants à 0 saut est plus complexe, mais pourrait révéler des informations similaires (bien qu'elle soit légèrement plus difficile à monter).

### tunnels à 1 saut

Avec seulement un router distant dans un tunnel, l'utilisateur bénéficie à la fois d'un déni plausible et d'un anonymat de base, tant qu'il ne fait pas face à un adversaire interne (comme décrit dans le [modèle de menace](/docs/overview/threat-model/)). Cependant, si l'adversaire contrôlait un nombre suffisant de routers tel que le router distant unique dans le tunnel soit souvent l'un de ces routers compromis, il pourrait alors monter l'attaque d'analyse statistique du trafic décrite ci-dessus.

### tunnels à 2 sauts

Avec deux ou plusieurs routers distants dans un tunnel, les coûts de mise en œuvre de l'attaque par analyse de trafic augmentent, car de nombreux routers distants devraient être compromis pour la réaliser.

### Tunnels à 3 sauts (ou plus)

Pour réduire la vulnérabilité à [certaines attaques](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/), 3 sauts ou plus sont recommandés pour un niveau de protection maximal. [Des études récentes](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) concluent également qu'au-delà de 3 sauts, aucune protection supplémentaire n'est apportée.

### Longueurs par défaut des tunnels

Le router utilise des tunnels à 2 bonds par défaut pour ses tunnels exploratoires. Les paramètres par défaut des tunnels clients sont définis par l'application, en utilisant les [options I2CP](/docs/specs/i2cp/#options). La plupart des applications utilisent 2 ou 3 bonds comme valeur par défaut.

---

## Test des tunnels

Tous les tunnels sont périodiquement testés par leur créateur en envoyant un DeliveryStatusMessage via un tunnel sortant et destiné à un autre tunnel entrant (testant ainsi les deux tunnels à la fois). Si l'un d'eux échoue à un nombre consécutif de tests, il est marqué comme n'étant plus fonctionnel. S'il était utilisé pour le tunnel entrant d'un client, un nouveau leaseSet est créé. Les échecs de test de tunnel se reflètent également dans l'[évaluation de capacité du profil de pair](/docs/overview/peer-selection/#capacity).

---

La création de tunnel est gérée par [garlic routing](/docs/overview/garlic-routing/) un Tunnel Build Message vers un router, demandant qu'il participe au tunnel (en lui fournissant toutes les informations appropriées, comme ci-dessus, ainsi qu'un certificat, qui est actuellement un certificat 'null', mais qui prendra en charge hashcash ou d'autres certificats non gratuits si nécessaire). Ce router transmet le message au saut suivant dans le tunnel. Les détails se trouvent dans la [spécification de création de tunnel](/docs/specs/tunnel-creation/).

## Création de tunnel

---

Le chiffrement multi-couches est géré par le [garlic encryption](/docs/overview/garlic-routing/) des messages de tunnel. Les détails se trouvent dans la [spécification des tunnels](/docs/specs/tunnel-implementation/). L'IV de chaque saut est chiffré avec une clé séparée comme expliqué là-bas.

## Chiffrement de tunnel

---

---

## Travaux futurs

- D'autres techniques de test de tunnel pourraient être utilisées, telles que l'emballage garlic encryption d'un certain nombre de tests en cloves, le test des participants individuels du tunnel séparément, etc.

- Passer par défaut aux tunnels exploratoires à 3 sauts.

- Dans une version future lointaine, des options spécifiant les paramètres de regroupement, de mélange et de génération de chaff pourraient être implémentées.

- Dans une version future lointaine, des limites sur la quantité et la taille des messages autorisés pendant la durée de vie du tunnel pourraient être implémentées (par exemple, pas plus de 300 messages ou 1 Mo par minute).

---

## Voir Aussi

- [Spécification des tunnels](/docs/specs/tunnel-implementation/)
- [Spécification de création de tunnel](/docs/specs/tunnel-creation/)
- [Tunnels unidirectionnels](/docs/legacy/unidirectional/)
- [Spécification des messages de tunnel](/docs/specs/tunnel-message/)
- [Routage garlic](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [Options I2CP](/docs/specs/i2cp/#options)
