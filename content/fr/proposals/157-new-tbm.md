---
title: "Messages de Construction de Tunnel Plus Petites"
number: "157"
author: "zzz, original"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Fermé"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
toc: true
---

## Remarque
Implémenté à partir de la version API 0.9.51.
Déploiement et tests réseau en cours.
Sujet à des révisions mineures.
Voir [I2NP](/docs/specs/i2np/) et [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) pour la spécification finale.


## Vue d'ensemble


### Résumé

La taille actuelle des enregistrements chiffrés de requête et de réponse de construction de tunnel est de 528.
Pour les messages typiques de construction de tunnel variable et de réponse de construction de tunnel variable,
la taille totale est de 2113 octets. Ce message est fragmenté en trois messages tunnel de 1 Ko pour le chemin inverse.

Les modifications du format d'enregistrement de 528 octets pour les routeurs ECIES-X25519 sont spécifiées dans [Prop152](/proposals/152-ecies-tunnels/) et [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).
Pour un mix de routeurs ElGamal et ECIES-X25519 dans un tunnel, la taille de l'enregistrement doit rester
à 528 octets. Cependant, si tous les routeurs dans un tunnel sont ECIES-X25519, un nouvel enregistrement de construction plus petit est possible, car le chiffrement ECIES-X25519 a beaucoup moins de surcharge
qu'ElGamal.

Des messages plus petits permettraient d'économiser de la bande passante. De plus, si les messages pouvaient tenir dans un seul message tunnel, le chemin inverse serait trois fois plus efficace.

Cette proposition définit les nouveaux enregistrements de requête et de réponse et les nouveaux messages de demande de construction et de réponse.

Le créateur de tunnel et tous les sauts dans le tunnel créé doivent être ECIES-X25519, et au moins en version 0.9.51.
Cette proposition ne sera utile que lorsqu'une majorité des routeurs dans le réseau sera ECIES-X25519.
Cela devrait se produire d'ici à fin 2021.


### Objectifs

Voir [Prop152](/proposals/152-ecies-tunnels/) et [Prop156](/proposals/156-ecies-routers/) pour des objectifs supplémentaires.

- Enregistrements et messages plus petits
- Maintenir un espace suffisant pour les options futures, comme dans [Prop152](/proposals/152-ecies-tunnels/) et [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
- Tenir dans un message tunnel pour le chemin inverse
- Supporter uniquement les sauts ECIES
- Maintenir les améliorations mises en œuvre dans [Prop152](/proposals/152-ecies-tunnels/) et [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
- Maximiser la compatibilité avec le réseau actuel
- Cacher les messages de construction entrants de l'OBEP
- Cacher les messages de réponse de construction sortants de l'IBGW
- Ne pas nécessiter de mise à jour "jour J" pour tout le réseau
- Déploiement progressif pour minimiser les risques
- Réutiliser les primitives cryptographiques existantes


### Non-Objectifs

Voir [Prop156](/proposals/156-ecies-routers/) pour des non-objectifs supplémentaires.

- Pas de nécessité de tunnels mixtes ElGamal/ECIES
- Changements de chiffrement de couche, pour cela voir [Prop153](/proposals/153-chacha20-layer-encryption/)
- Pas d'accélération des opérations cryptographiques. On suppose que ChaCha20 et AES sont similaires,
  même avec AESNI, du moins pour les petites tailles de données en question.


## Conception


### Enregistrements

Voir l'annexe pour les calculs.

Les enregistrements de requête et de réponse chiffrés feront 218 octets, par rapport à 528 octets actuellement.

Les enregistrements de requête en clair feront 154 octets,
par rapport à 222 octets pour les enregistrements ElGamal,
et 464 octets pour les enregistrements ECIES tels que définis dans [Prop152](/proposals/152-ecies-tunnels/) et [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).

Les enregistrements de réponse en clair feront 202 octets,
par rapport à 496 octets pour les enregistrements ElGamal,
et 512 octets pour les enregistrements ECIES tels que définis dans [Prop152](/proposals/152-ecies-tunnels/) et [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).

Le chiffrement de réponse sera ChaCha20 (PAS ChaCha20/Poly1305),
donc les enregistrements en clair n'ont pas besoin d'être un multiple de 16 octets.

Les enregistrements de requête seront rendus plus petits en utilisant HKDF pour créer les
couches et les clés de réponse, donc ils n'ont pas besoin d'être explicitement inclus dans la requête.


### Messages de Construction de Tunnel

Les deux seront "variables" avec un champ de nombre d'enregistrements d'un octet,
comme pour les messages variables existants.

#### ShortTunnelBuild: Type 25

Longueur typique (avec 4 enregistrements): 873 octets

Lorsqu'il est utilisé pour les constructions de tunnel entrant,
il est recommandé (mais pas obligatoire) que ce message soit chiffré à l'ail par l'initiateur,
ciblant la passerelle d'entrée (instructions de livraison ROUTER),
pour cacher les messages de construction entrants de l'OBEP.
L'IBGW décrypte le message,
place la réponse dans le bon emplacement,
et envoie le ShortTunnelBuildMessage à l'étape suivante.

La longueur de l'enregistrement est choisie de sorte qu'un STBM chiffré à l'ail tienne
dans un seul message de tunnel. Voir l'annexe ci-dessous.


#### OutboundTunnelBuildReply: Type 26

Nous définissons un nouveau message de réponse de construction de tunnel sortant.
Il est utilisé uniquement pour les constructions de tunnel sortant.
L'objectif est de cacher les messages de réponse de construction sortant de l'IBGW.
Il doit être chiffré à l'ail par l'OBEP, en ciblant l'initiateur
(instructions de livraison TUNNEL).
L'OBEP décrypte le message de construction de tunnel,
construit un message de réponse de construction de tunnel sortant,
et place la réponse dans le champ de texte en clair.
Les autres enregistrements vont dans les autres emplacements.
Il chiffre ensuite à l'ail le message à l'initiateur avec les clés symétriques dérivées.


#### Notes

En chiffrant à l'ail le OTBRM et le STBM, nous évitons également tout problème potentiel
de compatibilité à l'IBGW et à l'OBEP des tunnels jumelés.


### Flux de Message


```
STBM: Message de construction de court tunnel (type 25)
OTBRM: Message de réponse de construction de tunnel sortant (type 26)

Construction sortante A-B-C
Réponse via le tunnel entrant existant D-E-F


                Nouveau Tunnel
         STBM      STBM      STBM
Créateur ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Chiffré à l'ail
                                          | OTBRM
                                          | (livraison TUNNEL)
                                          | de OBEP à
                                          | créateur
              Tunnel Existant             /
Créateur <-------F---------E-------- D <--/
                                   IBGW


Construction Entrante D-E-F
Envoyé via le tunnel sortant existant A-B-C


              Tunnel Existant
Créateur ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Chiffré à l'ail (optionnel)
                                          | STBM
                                          | (livraison ROUTER)
                                          | du créateur
                Nouveau Tunnel            | à l'IBGW
          STBM      STBM      STBM        /
Créateur <------ F <------ E <------ D <--/
                                   IBGW


```


### Chiffrement des Enregistrements

Chiffrement des enregistrements de requête et de réponse : comme défini dans [Prop152](/proposals/152-ecies-tunnels/) et [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).

Chiffrement des enregistrements de réponse pour les autres emplacements : ChaCha20.


### Chiffrement de Couche

Actuellement, il n'y a pas de plan pour changer le chiffrement de couche pour les tunnels construits avec
cette spécification ; il resterait AES, comme actuellement utilisé pour tous les tunnels.

Changer le chiffrement de couche en ChaCha20 est un sujet de recherche supplémentaire.


### Nouveau Message de Données de Tunnel

Actuellement, il n'y a pas de plan pour changer le message de données de tunnel de 1 Ko utilisé pour les tunnels construits avec
cette spécification.

Il pourrait être utile d'introduire un nouveau message I2NP plus grand ou de taille variable, en parallèle avec cette proposition,
à utiliser sur ces tunnels.
Cela réduirait le surcoût pour les gros messages.
C'est un sujet de recherche supplémentaire.


## Spécification


### Enregistrement de Courte Requête


#### Enregistrement de Courte Requête Non Chiffré

Ceci est la spécification proposée de l'enregistrement de requête de construction de tunnel pour les routeurs ECIES-X25519.
Résumé des changements par rapport à [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies):

- Modifier la longueur non chiffrée de 464 à 154 octets
- Modifier la longueur chiffrée de 528 à 218 octets
- Supprimer les couches et les clés de réponse et les IVs, ils seront générés à partir de split() et d'un KDF


L'enregistrement de requête ne contient pas de clés de réponse ChaCha.
Ces clés sont dérivées d'un KDF. Voir ci-dessous.

Tous les champs sont en big-endian.

Taille non chiffrée : 154 octets.


```
octets     0-3: identifiant de tunnel pour recevoir les messages, non nul
octets     4-7: prochain identifiant de tunnel, non nul
octets    8-39: hachage d'identité du prochain routeur
octet       40: drapeaux
octets   41-42: plus de drapeaux, inutilisés, définis à 0 pour la compatibilité
octet       43: type de chiffrement de couche
octets   44-47: heure de la requête (en minutes depuis l'époque, arrondie)
octets   48-51: expiration de la requête (en secondes depuis la création)
octets   52-55: prochain identifiant de message
octets    56-x: options de construction de tunnel (Mapping)
octets     x-x: autres données selon les drapeaux ou options
octets   x-153: remplissage aléatoire (voir ci-dessous)
```


Le champ de drapeaux est le même que celui défini dans [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies) et contient ce qui suit :

 Ordre des bits : 76543210 (bit 7 est le MSB)
 bit 7 : si défini, autoriser les messages de n'importe qui
 bit 6 : si défini, autoriser les messages vers n'importe qui, et envoyer la réponse au
        prochain saut spécifié dans un message de réponse de construction de tunnel
 bits 5-0 : Indéfini, doit être défini à 0 pour compatibilité avec des options futures

Le bit 7 indique que le saut sera une passerelle d'entrée (IBGW). Le bit 6
indique que le saut sera un point de sortie (OBEP). Si aucun des bits n'est
défini, le saut sera un participant intermédiaire. Les deux ne peuvent pas être définis simultanément.

Type de chiffrement de couche : 0 pour AES (comme dans les tunnels actuels) ;
1 pour futur (ChaCha ?)

L'expiration de la requête est pour la durée de tunnel variable future.
Pour l'instant, la seule valeur supportée est 600 (10 minutes).

La clé publique éphémère du créateur est une clé ECIES, en big-endian.
Elle est utilisée pour le KDF pour les couches d'IBGW et les clés de réponse et les IVs.
Cela n'est inclus que dans l'enregistrement en clair dans un message de construction de tunnel entrant.
Elle est requise car il n'y a pas de DH à cette couche pour l'enregistrement de construction.

Les options de construction de tunnel est une structure de Mapping telle que définie dans [Common](/docs/specs/common-structures/).
C'est pour une utilisation future. Aucune option n'est actuellement définie.
Si la structure de Mapping est vide, elle est de deux octets 0x00 0x00.
La taille maximum du Mapping (incluant le champ de longueur) est de 98 octets,
et la valeur maximum du champ de longueur du Mapping est de 96.


#### Enregistrement de Courte Requête Chiffré

Tous les champs sont en big-endian sauf pour la clé publique éphémère qui est en little-endian.

Taille chiffrée : 218 octets


```
octets    0-15: hachage d'identité tronqué du saut
octets   16-47: clé publique X25519 éphémère de l'expéditeur
octets  48-201: Enregistrement de Courte Requête Chiffré par ChaCha20
octets 202-217: MAC Poly1305
```


### Enregistrement de Courte Réponse


#### Enregistrement de Courte Réponse Non Chiffré

Ceci est la spécification proposée de l'enregistrement de courte réponse de construction de tunnel pour les routeurs ECIES-X25519.
Résumé des changements par rapport à [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies):

- Modifier la longueur non chiffrée de 512 à 202 octets
- Modifier la longueur chiffrée de 528 à 218 octets


Les réponses ECIES sont chiffrées avec ChaCha20/Poly1305.

Tous les champs sont en big-endian.

Taille non chiffrée : 202 octets.


```
octets    0-x: Options de Réponse de Construction de Tunnel (Mapping)
octets    x-x: autres données selon les options
octets  x-200: Remplissage Aléatoire (voir ci-dessous)
octet     201: Octet de Réponse
```

Les options de réponse de construction de tunnel est une structure de Mapping telle que définie dans [Common](/docs/specs/common-structures/).
C'est pour une utilisation future. Aucune option n'est actuellement définie.
Si la structure de Mapping est vide, elle est de deux octets 0x00 0x00.
La taille maximum du Mapping (incluant le champ de longueur) est de 201 octets,
et la valeur maximum du champ de longueur du Mapping est de 199.

L'octet de réponse est une des valeurs suivantes
telles que définies dans [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies) pour éviter la collecte d'empreintes :

- 0x00 (acceptation)
- 30 (TUNNEL_REJECT_BANDWIDTH)


#### Enregistrement de Courte Réponse Chiffré

Taille chiffrée : 218 octets


```
octets   0-201: Enregistrement de Courte Réponse Chiffré par ChaCha20
octets 202-217: MAC Poly1305
```


### KDF

Voir la section KDF ci-dessous.


### ShortTunnelBuild
Type I2NP 25

Ce message est envoyé aux sauts intermédiaires, OBEP, et IBEP (créateur).
Il ne peut pas être envoyé à l'IBGW (utilisez plutôt le InboundTunnelBuild enveloppé à l'ail).
Lorsqu'il est reçu par l'OBEP, il est transformé en un OutboundTunnelBuildReply,
enveloppé à l'ail, et envoyé à l'initiateur.


```
+----+----+----+----+----+----+----+----+
| nombre| Enregistrements de Courte Réponse de Construction...
+----+----+----+----+----+----+----+----+

nombre ::
       1 octet `Entier`
       Valeurs valides : 1-8

taille de l'enregistrement : 218 octets
taille totale : 1+$nombre*218
```

#### Notes

* Nombre typique d'enregistrements est 4, pour une taille totale de 873.


### OutboundTunnelBuildReply
Type I2NP 26

Ce message est uniquement envoyé par l'OBEP à l'IBEP (créateur) via un tunnel entrant existant.
Il ne peut pas être envoyé à un autre saut.
Il est toujours enveloppé à l'ail.


```
+----+----+----+----+----+----+----+----+
| nombre|                                  |
+----+                                  +
|      Enregistrements de Courte Réponse de Construction...        |
+----+----+----+----+----+----+----+----+

nombre ::
       Nombre total d'enregistrements,
       1 octet `Entier`
       Valeurs valides : 1-8

Enregistrements de Courte Réponse de Construction ::
       Enregistrements chiffrés
       longueur : nombre * 218

taille de l'enregistrement chiffré : 218 octets
taille totale : 1+$nombre*218
```

#### Notes

* Nombre typique d'enregistrements est 4, pour une taille totale de 873.
* Ce message doit être enveloppé à l'ail.


### KDF

Nous utilisons ck de l'état de Noise après le chiffrement/déchiffrement de l'enregistrement de construction de tunnel
pour dériver les clés suivantes : clé de réponse, clé AES de couche, clé IV de couche AES et clé/étiquette de réponse à l'ail pour OBEP.

Clé de réponse :
Contrairement aux longs enregistrements, nous ne pouvons pas utiliser la partie gauche de ck pour la clé de réponse, car ce n'est pas la dernière et elle sera utilisée plus tard.
La clé de réponse est utilisée pour chiffrer cette réponse d'enregistrement en utilisant AEAD/Chaha20/Poly1305 et Chacha20 pour répondre aux autres enregistrements.
Les deux utilisent la même clé, le nonce est la position de l'enregistrement dans le message en commençant par 0.


```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

Clé de couche :
La clé de couche est toujours AES pour l'instant, mais le même KDF peut être utilisé pour Chacha20

keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

Clé IV pour enregistrement non-OBEP :
ivKey = keydata[0:31]
car c'est la dernière

Clé IV pour enregistrement OBEP :
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

Clé/étiquette de réponse à l'ail OBEP :
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
replyKey = keydata[32:63]
replyTag = keydata[0:7]
```


## Justification

Cette conception maximise la réutilisation des primitives cryptographiques, protocoles et codes existants.

Cette conception minimise les risques.

ChaCha20 est légèrement plus rapide que AES pour les petits enregistrements, dans les tests Java.
ChaCha20 évite une exigence de taille de données multiples de 16.


## Notes d'Implémentation

- Comme avec le message de construction de tunnel variable existant,
  les messages plus petits que 4 enregistrements ne sont pas recommandés.
  La valeur par défaut typique est de 3 sauts.
  Les tunnels entrants doivent être construits avec un enregistrement supplémentaire pour
  l'initiateur, afin que le dernier saut ne sache pas qu'il est le dernier.
  Pour que les sauts intermédiaires ne sachent pas si un tunnel est entrant ou sortant,
  les tunnels sortants devraient également être construits avec 4 enregistrements.


## Problèmes


## Migration

L'implémentation, les tests et le déploiement prendront plusieurs versions
et environ un an. Les phases sont les suivantes. L'affectation de
chaque phase à une version particulière est à déterminer et dépend de
la vitesse de développement.

Les détails de l'implémentation et la migration peuvent varier pour
chaque implémentation I2P.

Le créateur de tunnel doit s'assurer que tous les sauts dans le tunnel créé sont ECIES-X25519, ET sont au moins en version à déterminer.
Le créateur de tunnel ne doit PAS nécessairement être ECIES-X25519 ; il peut être ElGamal.
Cependant, si le créateur est ElGamal, cela révèle au saut le plus proche qu'il est le créateur.
Donc, en pratique, ces tunnels devraient uniquement être créés par des routeurs ECIES.

Il ne devrait PAS être nécessaire que le OBEP ou IBGW du tunnel jumelé soit ECIES ou
d'une version particulière.
Les nouveaux messages sont enveloppés à l'ail et ne sont pas visibles au OBEP ou IBGW
du tunnel jumelé.

Phase 1: Implémentation, non activée par défaut

Phase 2 (version suivante) : Activation par défaut

Il n'y a pas de problèmes de compatibilité descendante. Les nouveaux messages ne peuvent être envoyés qu'aux routeurs qui les supportent.


## Annexe


Sans surcharge d'ail pour un STBM entrant non chiffré,
si nous n'utilisons pas ITBM :


```
Taille actuelle 4 emplacements : 4 * 528 + surcharge = 3 messages tunnel

Message de construction de 4 emplacements pour tenir dans un message tunnel, uniquement ECIES :

1024
- 21 en-tête de fragment
----
1003
- 35 instructions de livraison non fragmentées ROUTER
----
968
- 16 en-tête I2NP
----
952
- 1 nombre d'emplacements
----
951
/ 4 emplacements
----
237 Nouvelle taille d'enregistrement de construction chiffré (vs. 528 maintenant)
- 16 hachage trunc.
- 32 clé éph.
- 16 MAC
----
173 taille maximum d'enregistrement de construction en clair (vs. 222 maintenant)


```


Avec surcharge d'ail pour le modèle de bruit 'N' pour chiffrer le STBM entrant,
si nous n'utilisons pas ITBM :


```
Taille actuelle 4 emplacements : 4 * 528 + surcharge = 3 messages tunnel

Message de construction chiffré à l'ail de 4 emplacements pour tenir dans un message tunnel, uniquement ECIES :

1024
- 21 en-tête de fragment
----
1003
- 35 instructions de livraison non fragmentées ROUTER
----
968
- 16 en-tête I2NP
-  4 longueur
----
948
- 32 octets clé éph.
----
916
- 7 octets bloc DateTime
----
909
- 3 octets surcharge bloc Garlic
----
906
- 9 octets en-tête I2NP
----
897
- 1 octet Garlic instructions de livraison LOCALE
----
896
- 16 octets MAC Poly1305
----
880
- 1 nombre d'emplacements
----
879
/ 4 emplacements
----
219 Nouvelle taille d'enregistrement de construction chiffré (vs. 528 maintenant)
- 16 hachage trunc.
- 32 clé éph.
- 16 MAC
----
155 taille maximum d'enregistrement de construction en clair (vs. 222 maintenant)

```

Notes :

Taille actuelle de l'enregistrement de construction en clair avant le remplissage inutilisé: 193

La suppression du hachage complet du routeur et la génération HKDF de clés/IV libéreraient beaucoup de place pour les options futures.
Si tout est HKDF, l'espace requis en clair est d'environ 58 octets (sans aucune option).

Le OTBRM enveloppé à l'ail sera légèrement plus petit que le STBM enveloppé à l'ail,
car les instructions de livraison sont LOCALE et non ROUTER,
il n'y a pas de bloc DATETIME inclus, et
il utilise une étiquette de 8 octets plutôt que la clé éphémère de 32 octets pour un message 'N' complet.


## Références
