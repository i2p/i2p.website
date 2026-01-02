---
title: "Routage de Tunnel"
description: "Aperçu de la terminologie, construction et cycle de vie des tunnels I2P"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Aperçu

I2P construit des tunnels temporaires et unidirectionnels — des séquences ordonnées de routeurs qui transmettent du trafic chiffré. Les tunnels sont classés comme **entrants** (les messages circulent vers le créateur) ou **sortants** (les messages circulent depuis le créateur).

Un échange typique achemine le message d'Alice à travers l'un de ses tunnels sortants, ordonne au point de sortie de le transférer vers la passerelle de l'un des tunnels entrants de Bob, puis Bob le reçoit à son point d'entrée.

![Alice se connectant via son tunnel sortant à Bob via son tunnel entrant](/images/tunnelSending.png)

- **A** : Gateway sortant (Alice)
- **B** : Participant sortant
- **C** : Point terminal sortant
- **D** : Gateway entrant
- **E** : Participant entrant
- **F** : Point terminal entrant (Bob)

Les tunnels ont une durée de vie fixe de 10 minutes et transportent des messages de taille fixe de 1024 octets (1028 octets en incluant l'en-tête du tunnel) afin d'empêcher l'analyse de trafic basée sur la taille des messages ou les modèles temporels.

## Vocabulaire des tunnels

- **Tunnel gateway:** Premier router dans un tunnel. Pour les tunnels entrants, l'identité de ce router apparaît dans le [LeaseSet](/docs/specs/common-structures/) publié. Pour les tunnels sortants, le gateway est le router d'origine (A et D ci-dessus).
- **Tunnel endpoint:** Dernier router dans un tunnel (C et F ci-dessus).
- **Tunnel participant:** Router intermédiaire dans un tunnel (B et E ci-dessus). Les participants ne peuvent pas déterminer leur position ni la direction du tunnel.
- **Tunnel n-hop:** Nombre de sauts inter-router.
  - **0-hop:** Gateway et endpoint sont le même router – anonymat minimal.
  - **1-hop:** Gateway se connecte directement au endpoint – faible latence, faible anonymat.
  - **2-hop:** Par défaut pour les tunnels exploratoires ; sécurité/performance équilibrée.
  - **3-hop:** Recommandé pour les applications nécessitant un anonymat élevé.
- **Tunnel ID:** Entier de 4 octets unique par router et par saut, choisi aléatoirement par le créateur. Chaque saut reçoit et transmet sur des ID différents.

## Informations de construction de tunnel

Les routeurs remplissant les rôles de passerelle, participant et point de terminaison reçoivent différents enregistrements dans le Tunnel Build Message. I2P moderne prend en charge deux méthodes :

- **ElGamal** (ancien, enregistrements de 528 octets)
- **ECIES-X25519** (actuel, enregistrements de 218 octets via Short Tunnel Build Message – STBM)

### Information Distributed to Participants

**Le gateway reçoit :** - Clé de couche tunnel (clé AES-256 ou ChaCha20 selon le type de tunnel) - Clé IV du tunnel (pour chiffrer les vecteurs d'initialisation) - Clé de réponse et IV de réponse (pour le chiffrement de la réponse de construction) - ID du tunnel (gateways entrants uniquement) - Hash d'identité du prochain saut et ID du tunnel (si non-terminal)

**Les participants intermédiaires reçoivent :** - La clé de couche tunnel et la clé IV pour leur saut - L'ID du tunnel et les informations sur le prochain saut - La clé de réponse et l'IV pour le chiffrement de la réponse de construction

**Les endpoints reçoivent :** - Les clés de couche tunnel et IV - Le routeur de réponse et l'ID du tunnel (endpoints sortants uniquement) - La clé de réponse et l'IV (endpoints sortants uniquement)

Pour plus de détails, consultez la [Spécification de création de tunnel](/docs/specs/implementation/) et la [Spécification de création de tunnel ECIES](/docs/specs/implementation/).

## Tunnel Pooling

Les routeurs regroupent les tunnels en **pools de tunnels** pour la redondance et la distribution de charge. Chaque pool maintient plusieurs tunnels parallèles, permettant le basculement lorsqu'un tunnel échoue. Les pools utilisés en interne sont les **tunnels exploratoires** (exploratory tunnels), tandis que les pools spécifiques aux applications sont les **tunnels clients** (client tunnels).

Chaque destination maintient des pools entrants et sortants séparés, configurés par les options I2CP (nombre de tunnels, nombre de sauvegardes, longueur et paramètres QoS). Les routeurs surveillent l'état des tunnels, effectuent des tests périodiques et reconstruisent automatiquement les tunnels défaillants pour maintenir la taille du pool.

## Mutualisation des tunnels

**Tunnels à 0 saut** : Offrent uniquement un déni plausible. Le trafic provient toujours du même router et s'y termine — déconseillé pour toute utilisation anonyme.

**Tunnels à 1 saut** : Offrent une anonymité de base contre les observateurs passifs mais sont vulnérables si un adversaire contrôle ce saut unique.

**Tunnels à 2 sauts** : Incluent deux routeurs distants et augmentent considérablement le coût d'une attaque. Par défaut pour les pools exploratoires.

**Tunnels à 3 sauts** : Recommandés pour les applications nécessitant une protection robuste de l'anonymat. Des sauts supplémentaires ajoutent de la latence sans gain de sécurité significatif.

**Par défaut** : Les routeurs utilisent des tunnels exploratoires à **2 sauts** et des tunnels clients spécifiques aux applications à **2 ou 3 sauts**, équilibrant performance et anonymat.

## Longueur du tunnel

Les routeurs testent périodiquement les tunnels en envoyant un `DeliveryStatusMessage` à travers un tunnel sortant vers un tunnel entrant. Si le test échoue, les deux tunnels reçoivent un poids de profil négatif. Des échecs consécutifs marquent un tunnel comme inutilisable ; le routeur reconstruit alors un remplaçant et publie un nouveau LeaseSet. Les résultats alimentent les métriques de capacité des pairs utilisées par le [système de sélection des pairs](/docs/overview/tunnel-routing/).

## Test des tunnels

Les routeurs construisent des tunnels en utilisant une méthode de **telescoping** non interactive : un seul message Tunnel Build se propage saut par saut. Chaque saut déchiffre son enregistrement, ajoute sa réponse et transmet le message. Le saut final renvoie la réponse de construction agrégée via un chemin différent, empêchant la corrélation. Les implémentations modernes utilisent des **Short Tunnel Build Messages (STBM)** pour ECIES et des **Variable Tunnel Build Messages (VTBM)** pour les chemins legacy. Chaque enregistrement est chiffré par saut en utilisant ElGamal ou ECIES-X25519.

## Création de tunnel

Le trafic des tunnels utilise un chiffrement multi-couches. Chaque saut ajoute ou retire une couche de chiffrement au fur et à mesure que les messages traversent le tunnel.

- **Tunnels ElGamal :** AES-256/CBC pour les charges utiles avec remplissage PKCS#5.
- **Tunnels ECIES :** ChaCha20 ou ChaCha20-Poly1305 pour le chiffrement authentifié.

Chaque saut possède deux clés : une **clé de couche** et une **clé IV**. Les routeurs déchiffrent l'IV, l'utilisent pour traiter la charge utile, puis rechiffrent l'IV avant de le transmettre. Ce schéma de double IV empêche le marquage des messages.

Les passerelles sortantes pré-déchiffrent toutes les couches afin que les points de terminaison reçoivent du texte en clair après que tous les participants aient ajouté le chiffrement. Les tunnels entrants chiffrent dans la direction opposée. Les participants ne peuvent pas déterminer la direction ou la longueur du tunnel.

## Chiffrement des tunnels

- Durées de vie des tunnels dynamiques et dimensionnement adaptatif des pools pour l'équilibrage de charge réseau
- Stratégies alternatives de test des tunnels et diagnostics individuels des sauts
- Validation optionnelle par preuve de travail ou certificat de bande passante (implémenté dans l'API 0.9.65+)
- Recherche sur le façonnage du trafic et l'insertion de chaff pour le mélange des points de terminaison
- Retrait progressif d'ElGamal et migration vers ECIES-X25519

## Développement en cours

- [Spécification d'implémentation de tunnel](/docs/specs/implementation/)
- [Spécification de création de tunnel (ElGamal)](/docs/specs/implementation/)
- [Spécification de création de tunnel (ECIES-X25519)](/docs/specs/implementation/)
- [Spécification des messages de tunnel](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [Base de données réseau I2P (netDb)](/docs/specs/common-structures/)
- [Profilage et sélection des pairs](/docs/overview/tunnel-routing/)
- [Modèle de menace I2P](/docs/overview/threat-model/)
- [Chiffrement ElGamal/AES + SessionTag](/docs/legacy/elgamal-aes/)
- [Options I2CP](/docs/specs/i2cp/)
