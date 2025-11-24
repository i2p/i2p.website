---
title: "Tunnels ECIES"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Fermé"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## Remarque
Déploiement et test du réseau en cours.
Sujet à des révisions mineures.
Voir [SPEC](/en/docs/spec/) pour les spécifications officielles.


## Vue d'ensemble

Ce document propose des changements à l'encryption du message de construction de tunnel
en utilisant les primitives cryptographiques introduites par [ECIES-X25519](/en/docs/spec/ecies/).
Cela fait partie de la proposition globale
[Prop156](/en/proposals/156-ecies-routers/) pour convertir les routeurs d'ElGamal à des clés ECIES-X25519.

Dans le but de faire passer le réseau d'ElGamal + AES256 à ECIES + ChaCha20,
des tunnels avec des routeurs ElGamal et ECIES mixtes sont nécessaires.
Des spécifications pour le traitement des sauts de tunnels mixtes sont fournies.
Aucun changement ne sera apporté au format, au traitement ou à l'encryptage des sauts ElGamal.

Les créateurs de tunnels ElGamal devront créer des paires de clés X25519 éphémères par saut, et
suivre cette spécification pour créer des tunnels contenant des sauts ECIES.

Cette proposition spécifie les changements nécessaires pour la construction de tunnels ECIES-X25519.
Pour un aperçu de tous les changements requis pour les routeurs ECIES, voir la proposition 156 [Prop156](/en/proposals/156-ecies-routers/).

Cette proposition maintient la même taille pour les enregistrements de construction de tunnel,
comme requis pour la compatibilité. Des enregistrements et messages de construction plus petits seront
implémentés ultérieurement - voir [Prop157](/en/proposals/157-new-tbm/).


### Primitives cryptographiques

Aucune nouvelle primitive cryptographique n'est introduite. Les primitives nécessaires pour implémenter cette proposition sont :

- AES-256-CBC comme dans [Cryptography](/en/docs/spec/cryptography/)
- Fonctions STREAM ChaCha20/Poly1305 :
  ENCRYPT(k, n, plaintexte, ad) et DECRYPT(k, n, chiffretexte, ad) - comme dans [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) et [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Fonctions DH X25519 - comme dans [NTCP2](/en/docs/spec/ntcp2/) et [ECIES-X25519](/en/docs/spec/ecies/)
- HKDF(salt, ikm, info, n) - comme dans [NTCP2](/en/docs/spec/ntcp2/) et [ECIES-X25519](/en/docs/spec/ecies/)

Autres fonctions Noise définies ailleurs :

- MixHash(d) - comme dans [NTCP2](/en/docs/spec/ntcp2/) et [ECIES-X25519](/en/docs/spec/ecies/)
- MixKey(d) - comme dans [NTCP2](/en/docs/spec/ntcp2/) et [ECIES-X25519](/en/docs/spec/ecies/)


### Objectifs

- Augmenter la vitesse des opérations cryptographiques
- Remplacer ElGamal + AES256/CBC par des primitives ECIES pour les BuildRequestRecords de tunnel et les BuildReplyRecords.
- Pas de changement de taille des BuildRequestRecords et BuildReplyRecords encryptés (528 octets) pour la compatibilité
- Pas de nouveaux messages I2NP
- Maintenir la taille des enregistrements de construction encryptés pour la compatibilité
- Ajouter une secret de redirection pour les messages de construction de tunnel.
- Ajouter un chiffrement authentifié
- Détecter les réorganisations de sauts des BuildRequestRecords
- Augmenter la résolution du timestamp pour que la taille du filtre Bloom puisse être réduite
- Ajouter un champ pour l'expiration du tunnel pour que des durées de tunnel variables soient possibles (tunnels entièrement ECIES uniquement)
- Ajouter un champ d'options extensibles pour les fonctionnalités futures
- Réutiliser les primitives cryptographiques existantes
- Améliorer la sécurité des messages de construction de tunnel autant que possible tout en maintenant la compatibilité
- Supporter les tunnels avec des pairs ElGamal/ECIES mixtes
- Améliorer les défenses contre les attaques par "tagging" sur les messages de construction
- Les sauts n'ont pas besoin de connaître le type d'encryption du prochain saut avant de traiter le message de construction,
  car il se peut qu'ils n'aient pas l'RI du prochain saut à ce moment-là
- Maximiser la compatibilité avec le réseau actuel
- Pas de changement à l'encryption de requête/réponse AES de construction de tunnel pour les routeurs ElGamal
- Pas de changement à l'encryption AES "couche" de tunnel, pour cela voir [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Continuer à supporter la taille variable 8-record TBM/TBRM et VTBM/VTBRM
- Ne pas exiger la mise à jour de l'intégralité du réseau pour un "jour du drapeau"


### Non-objectifs

- Redesign complet des messages de construction de tunnel nécessitant un "jour du drapeau".
- Réduction de la taille des messages de construction de tunnel (nécessite tous les sauts ECIES et une nouvelle proposition)
- Utilisation des options de construction de tunnel comme définies dans [Prop143](/en/proposals/143-build-message-options/), seulement nécessaires pour les petits messages
- Tunnels bidirectionnels - pour cela voir [Prop119](/en/proposals/119-bidirectional-tunnels/)
- Messages de construction de tunnel plus petits - pour cela voir [Prop157](/en/proposals/157-new-tbm/)


## Modèle de menace

### Objectifs de conception

- Aucun saut ne doit être en mesure de déterminer l'origine du tunnel.

- Les sauts intermédiaires ne doivent pas pouvoir déterminer la direction du tunnel
  ou leur position dans le tunnel.

- Aucun saut ne peut lire le contenu d'autres enregistrements de requête ou de réponse, sauf
  pour le hash du routeur tronqué et la clé éphémère pour le prochain saut

- Aucun membre du tunnel de réponse pour la construction sortante ne peut lire un enregistrement de réponse.

- Aucun membre du tunnel sortant pour la construction entrante ne peut lire un enregistrement de requête,
  sauf que OBEP peut voir le hash du routeur tronqué et la clé éphémère pour IBGW




### Attaques par tagging

Un objectif majeur de la conception de la construction de tunnel est de rendre plus difficile
pour les routeurs collusoires X et Y de savoir qu'ils sont dans un seul tunnel.
Si le routeur X est au saut m et le routeur Y est au saut m+1, ils le sauront évidemment.
Mais si le routeur X est au saut m et le routeur Y est au saut m+n pour n>1, cela devrait être beaucoup plus difficile.

Les attaques de tagging consistent en ce que le routeur intermédiaire X altère le message de construction de tunnel de telle manière que
le routeur Y puisse détecter l'altération lorsque le message de construction y arrive.
L'objectif est qu'un message altéré soit rejeté par un routeur entre X et Y avant qu'il n'arrive au routeur Y.
Pour les modifications qui ne sont pas rejetées avant d'arriver au routeur Y, le créateur du tunnel devrait détecter la corruption dans la réponse
et abandonner le tunnel.

Attaques possibles :

- Modifier un enregistrement de construction
- Remplacer un enregistrement de construction
- Ajouter ou supprimer un enregistrement de construction
- Réorganiser les enregistrements de construction





TODO: La conception actuelle empêche-t-elle toutes ces attaques?






## Conception

### Cadre du protocole Noise

Cette proposition fournit les exigences basées sur le cadre du protocole Noise
[NOISE](https://noiseprotocol.org/noise.html) (Révision 34, 2018-07-11).
Dans le parlance Noise, Alice est l'initiateur, et Bob est le répondeur.

Cette proposition est basée sur le protocole Noise Noise_N_25519_ChaChaPoly_SHA256.
Ce protocole Noise utilise les primitives suivantes :

- Modèle de poignée de main unidirectionnelle : N  
  Alice ne transmet pas sa clé statique à Bob (N)

- Fonction DH : X25519  
  X25519 DH avec une longueur de clé de 32 octets comme spécifié dans [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Fonction de chiffrement : ChaChaPoly  
  AEAD_CHACHA20_POLY1305 comme spécifié dans [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8.
  Nonce de 12 octets, avec les premiers 4 octets mis à zéro.
  Identique à celle dans [NTCP2](/en/docs/spec/ntcp2/).

- Fonction de hachage : SHA256  
  Hachage standard de 32 octets, déjà utilisé extensivement dans I2P.


Ajouts au cadre
``````````````````````````

Aucun.


### Modèles de poignée de main

Les poignées de main utilisent les modèles de poignée de main [Noise].

La cartographie de lettres suivante est utilisée :

- e = clé éphémère unique
- s = clé statique
- p = chargement du message

La demande de construction est identique au modèle Noise N.
Ceci est également identique au premier message (Demande de session) dans le modèle XK utilisé dans [NTCP2](/en/docs/spec/ntcp2/).


  ```dataspec

<- s
  ...
  e es p ->





  ```


### Chiffrement des demandes

Les enregistrements de demande de construction sont créés par le créateur de tunnel et asymétriquement encryptés pour le saut individuel.
Cette encryption asymétrique des enregistrements de demande est actuellement ElGamal comme défini dans [Cryptography](/en/docs/spec/cryptography/)
et contient une somme de contrôle SHA-256. Cette conception n'est pas secrète en avant.

La nouvelle conception utilisera le modèle Noise unidirectionnel "N" avec ECIES-X25519 DH éphémère-statique, avec un HKDF, et
ChaCha20/Poly1305 AEAD pour le secret en avant, l'intégrité, et l'authentification.
Alice est le demandeur de construction de tunnel. Chaque saut dans le tunnel est un Bob.


(Propriétés de sécurité du chargement)

  ```text

N:                      Authentification   Confidentialité
    -> e, es                  0                2

    Authentification : Aucune (0).
    Ce chargement peut avoir été envoyé par n'importe quelle partie, y compris un attaquant actif.

    Confidentialité : 2.
    Chiffrement pour un destinataire connu, secret en avant pour la compromission de l'expéditeur
    uniquement, vulnérable à la relecture. Ce chargement est encrypté basée seulement sur les DHe
    impliquant la paire de clés statiques du destinataire. Si la clé privée statique du destinataire est compromise,
    même à une date ultérieure, ce chargement peut être décrypté. Ce message peut également être relu, car il n'y a pas de contribution éphémère du destinataire.

    "e" : Alice génère une nouvelle paire de clés éphémères et la stocke dans la
         variable e, écrit la clé publique éphémère comme texte clair dans
         le tampon de message, et hache la clé publique avec l'ancien h pour
         dériver un nouveau h.

    "es" : Un DH est effectué entre la paire de clés éphémères d'Alice et
          la paire de clés statiques de Bob. Le résultat est haché avec l'ancien ck pour
          dériver un nouveau ck et k, et n est mis à zéro.






  ```



### Chiffrement des réponses

Les enregistrements de réponse de construction sont créés par le créateur de sauts et symétriquement encryptés pour le créateur.
Cette encryption symétrique des enregistrements de réponse est actuellement AES avec un contrôle SHA-256 préfixé.
et contient une somme de contrôle SHA-256. Cette conception n'est pas secrète en avant.

La nouvelle conception utilisera ChaCha20/Poly1305 AEAD pour l'intégrité, et l'authentification.


### Justification

La clé publique éphémère dans la demande n'a pas besoin d'être obscurcie avec AES
ou Elligator2. Le saut précédent est le seul qui peut la voir, et ce saut
sait que le saut suivant est ECIES.

Les enregistrements de réponse n'ont pas besoin de l'encryption asymétrique complète avec un autre DH.



## Spécification



### Enregistrements de requêtes de construction

Les enregistrements BuildRequest encryptés ont une taille de 528 octets pour ElGamal et ECIES, pour la compatibilité.


Enregistrement de requête non encrypté (ElGamal)
```````````````````````````````````````````

A titre de référence, voici la spécification actuelle de l'enregistrement BuildRequest de tunnel pour les routeurs ElGamal, tirée de [I2NP](/en/docs/spec/i2np/).
Les données non encryptées sont précédées d'un octet non nul et du hash SHA-256 des données avant l'encryption,
comme défini dans [Cryptography](/en/docs/spec/cryptography/).

Tous les champs sont en big-endian.

Taille non encryptée : 222 octets

  ```dataspec


octets     0-3: ID de tunnel pour recevoir les messages, non nul
  octets    4-35: hash d'identité du routeur local
  octets   36-39: prochain ID de tunnel, non nul
  octets   40-71: prochain hash d'identité du routeur
  octets  72-103: clé de couche de tunnel AES-256
  octets 104-135: clé de IV de tunnel AES-256
  octets 136-167: clé de réponse AES-256
  octets 168-183: IV de réponse AES-256
  octet      184: drapeaux
  octets 185-188: heure de la demande (en heures depuis l'époque, arrondie)
  octets 189-192: prochain ID de message
  octets 193-221: remplissage aléatoire / non interprété




  ```


Enregistrement de requête encrypté (ElGamal)
```````````````````````````````````````````

A titre de référence, voici la spécification actuelle de l'enregistrement BuildRequest de tunnel pour les routeurs ElGamal, tirée de [I2NP](/en/docs/spec/i2np/).

Taille encryptée : 528 octets

  ```dataspec


octets    0-15: hash d'identité tronqué du saut
  octets  16-528: BuildRequestRecord encrypté avec ElGamal




  ```




Enregistrement de requête non encrypté (ECIES)
```````````````````````````````````````````

Voici la spécification proposée de l'enregistrement BuildRequest de tunnel pour les routeurs ECIES-X25519.
Résumé des changements :

- Supprimer le hash de routeur 32 octets inutilisé
- Changer l'heure de la demande de heures à minutes
- Ajouter un champ d'expiration pour la durée de tunnel future variable
- Ajouter plus d'espace pour les drapeaux
- Ajouter un Mapping pour des options de construction supplémentaires
- La clé et IV de réponse AES-256 ne sont pas utilisées pour l'enregistrement de réponse du saut propre
- L'enregistrement non encrypté est plus long parce qu'il y a moins de surcharge d'encryption

L'enregistrement de requête ne contient pas de clés de réponse ChaCha.
Ces clés sont dérivées d'un KDF. Voir ci-dessous.

Tous les champs sont en big-endian.

Taille non encryptée : 464 octets

  ```dataspec


octets     0-3: ID de tunnel pour recevoir les messages, non nul
  octets     4-7: prochain ID de tunnel, non nul
  octets    8-39: hash d'identité du prochain routeur
  octets   40-71: clé de couche de tunnel AES-256
  octets  72-103: clé de IV de tunnel AES-256
  octets 104-135: clé de réponse AES-256
  octets 136-151: IV de réponse AES-256
  octet      152: drapeaux
  octets 153-155: plus de drapeaux, non utilisés, mis à 0 pour compatibilité
  octets 156-159: heure de la demande (en minutes depuis l'époque, arrondie)
  octets 160-163: expiration de la demande (en secondes depuis la création)
  octets 164-167: prochain ID de message
  octets   168-x: options de construction de tunnel (Mapping)
  octets     x-x: autres données comme impliquées par les drapeaux ou options
  octets   x-463: remplissage aléatoire




  ```

Le champ de drapeaux est le même que celui défini dans [Tunnel-Creation](/en/docs/spec/tunnel-creation/) et contient ce qui suit ::

 Ordre des bits : 76543210 (bit 7 est MSB)
 bit 7: si configuré, permet les messages de tout le monde
 bit 6: si configuré, permet les messages à tout le monde et envoie la réponse au
        prochain saut spécifié dans un message de réponse de construction de tunnel
 bits 5-0 : Non défini, doivent être configurés à 0 pour la compatibilité avec les futures options

Le bit 7 indique que le saut sera une passerelle entrante (IBGW). Le bit 6
indique que le saut sera un point final sortant (OBEP). Si aucun bit n'est
attribué, le saut sera un participant intermédiaire. Les deux ne peuvent pas être configurés en même temps.

L'expiration de la demande est pour la durée variable future du tunnel.
Pour le moment, la seule valeur prise en charge est 600 (10 minutes).

Les options de construction de tunnel sont une structure de Mapping comme définie dans [Common](/en/docs/spec/common-structures/).
C'est pour une utilisation future. Aucune option n'est actuellement définie.
Si la structure de Mapping est vide, cela correspond à deux octets 0x00 0x00.
La taille maximale du Mapping (y compris le champ de longueur) est de 296 octets,
et la valeur maximale du champ de longueur du Mapping est de 294.



Enregistrement de requête encrypté (ECIES)
```````````````````````````````````````````

Tous les champs sont en big-endian sauf pour la clé publique éphémère qui est en little-endian.

Taille encryptée : 528 octets

  ```dataspec


octets    0-15: hash d'identité tronqué du saut
  octets   16-47: clé publique X25519 éphémère de l'expéditeur
  octets  48-511: BuildRequestRecord encrypté avec ChaCha20
  octets 512-527: MAC Poly1305




  ```



### Enregistrements de réponse de construction

Les enregistrements BuildReply encryptés sont de 528 octets pour ElGamal et ECIES, pour la compatibilité.


Enregistrement de réponse non encrypté (ElGamal)
```````````````````````````````````````````
Les réponses ElGamal sont encryptées avec AES.

Tous les champs sont en big-endian.

Taille non encryptée : 528 octets

  ```dataspec


octets   0-31: Hash SHA-256 des octets 32-527
  octets 32-526: données aléatoires
  octet     527: réponse

  longueur totale : 528




  ```


Enregistrement de réponse non encrypté (ECIES)
```````````````````````````````````````````
Voici la spécification proposée de l'enregistrement BuildReplyRecord de tunnel pour les routeurs ECIES-X25519.
Résumé des changements :

- Ajouter un Mapping pour les options de réponse de construction
- L'enregistrement non encrypté est plus long car il y a moins de surcharge d'encryption

Les réponses ECIES sont encryptées avec ChaCha20/Poly1305.

Tous les champs sont en big-endian.

Taille non encryptée : 512 octets

  ```dataspec


octets    0-x: Options de réponse de construction de tunnel (Mapping)
  octets    x-x: autres données comme impliquées par les options
  octets  x-510: Remplissage aléatoire
  octet     511: Octet de réponse




  ```

Les options de réponse de construction de tunnel sont une structure de Mapping comme définie dans [Common](/en/docs/spec/common-structures/).
C'est pour une utilisation future. Aucune option n'est actuellement définie.
Si la structure de Mapping est vide, cela correspond à deux octets 0x00 0x00.
La taille maximale du Mapping (y compris le champ de longueur) est de 511 octets,
et la valeur maximale du champ de longueur du Mapping est de 509.

L'octet de réponse est l'une des valeurs suivantes
comme défini dans [Tunnel-Creation](/en/docs/spec/tunnel-creation/) pour éviter l'empreinte digitale :

- 0x00 (acceptation)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Enregistrement de réponse encrypté (ECIES)
```````````````````````````````````````````

Taille encryptée : 528 octets

  ```dataspec


octets   0-511: BuildReplyRecord encrypté avec ChaCha20
  octets 512-527: MAC Poly1305




  ```

Après la transition complète vers les enregistrements ECIES, les règles de remplissage en plage sont les mêmes que pour les enregistrements de demande.


### Encryption symétrique des enregistrements

Les tunnels mixtes sont autorisés, et nécessaires pour la transition d'ElGamal à ECIES.
Pendant la période de transition, un nombre croissant de routeurs seront sous clés ECIES.

Le prétraitement de la cryptographie symétrique fonctionnera de la même manière :

- "encryption" :

  - chiffrement exécuté en mode décryptage
  - les enregistrements de demande sont préemptivement décryptés lors du prétraitement (cachant les enregistrements de demande encryptés)

- "décryption" :

  - chiffrement exécuté en mode encryption
  - les enregistrements de demande sont encryptés (révélation du prochain enregistrement de demande en clair) par les sauts participants

- ChaCha20 n'a pas de "modes", il est donc simplement exécuté trois fois :

  - une fois lors du prétraitement
  - une fois par le saut
  - une fois lors du traitement de la réponse finale

Lorsque des tunnels mixtes sont utilisés, les créateurs de tunnels devront baser l'encryption symétrique
du BuildRequestRecord sur le type d'encryption du saut actuel et précédent.

Chaque saut utilisera son propre type d'encryption pour l'encryption des BuildReplyRecords, et des autres
enregistrements dans le VariableTunnelBuildMessage (VTBM).

Sur le chemin de retour, le point final (l'émetteur) devra annuler le [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), en utilisant la clé de réponse de chaque saut.

En tant qu'exemple clarificateur, examinons un tunnel sortant avec ECIES entouré par ElGamal :

- Expéditeur (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tous les BuildRequestRecords sont dans leur état encrypté (en utilisant ElGamal ou ECIES).

Le cipher AES256/CBC, lorsqu'il est utilisé, est encore utilisé pour chaque enregistrement, sans enchaînement à travers plusieurs enregistrements.

De même, ChaCha20 sera utilisé pour encrypter chaque enregistrement, sans mise en streaming à travers l'intégralité du VTBM.

Les enregistrements de demande sont prétraités par l'expéditeur (OBGW):

- L'enregistrement de H3 est "encrypté" en utilisant :

  - la clé de réponse de H2 (ChaCha20)
  - la clé de réponse de H1 (AES256/CBC)

- L'enregistrement de H2 est "encrypté" en utilisant :

  - la clé de réponse de H1 (AES256/CBC)

- L'enregistrement de H1 part sans encryption symétrique

Seul H2 vérifie le drapeau d'encryption de réponse, et voit que c'est suivi par AES256/CBC.

Après avoir été traités par chaque saut, les enregistrements sont dans un état "décrypté" :

- L'enregistrement de H3 est "décrypté" en utilisant :

  - la clé de réponse de H3 (AES256/CBC)

- L'enregistrement de H2 est "décrypté" en utilisant :

  - la clé de réponse de H3 (AES256/CBC)
  - la clé de réponse de H2 (ChaCha20-Poly1305)

- L'enregistrement de H1 est "décrypté" en utilisant :

  - la clé de réponse de H3 (AES256/CBC)
  - la clé de réponse de H2 (ChaCha20)
  - la clé de réponse de H1 (AES256/CBC)

Le créateur du tunnel, c'est-à-dire le point final entrant (IBEP), post-traite la réponse :

- L'enregistrement de H3 est "encrypté" en utilisant :

  - la clé de réponse de H3 (AES256/CBC)

- L'enregistrement de H2 est "encrypté" en utilisant :

  - la clé de réponse de H3 (AES256/CBC)
  - la clé de réponse de H2 (ChaCha20-Poly1305)

- L'enregistrement de H1 est "encrypté" en utilisant :

  - la clé de réponse de H3 (AES256/CBC)
  - la clé de réponse de H2 (ChaCha20)
  - la clé de réponse de H1 (AES256/CBC)


### Clés d'enregistrement de demande (ECIES)

Ces clés sont explicitement incluses dans les BuildRequestRecords ElGamal.
Pour les BuildRequestRecords ECIES, les clés de tunnel et les clés de réponse AES sont incluses,
mais les clés de réponse ChaCha sont dérivées de l'échange DH.
Voir [Prop156](/en/proposals/156-ecies-routers/) pour les détails des clés ECIES statiques de routeur.

Ci-dessous est une description de comment dériver les clés précédemment transmises dans les enregistrements de demande.


KDF pour le ck et h initial
``````````````````````````

Ceci est le standard [NOISE](https://noiseprotocol.org/noise.html) pour le modèle "N" avec un nom de protocole standard.

  ```text

Ceci est le modèle de message "e" :

  // Définir protocol_name.
  Définir protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 octets, encodé US-ASCII, sans terminaison NULL).

  // Définir Hash h = 32 octets
  // Remplir à 32 octets. Ne PAS hacher, car ce n'est pas plus que 32 octets.
  h = protocol_name || 0

  Définir ck = clé d'enchaînement de 32 octets. Copier les données de h dans ck.
  Définir chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // jusque-là, peut être précalculé par tous les routeurs.




  ```


KDF pour l'enregistrement de demande
````````````````````````````````````

Les créateurs de tunnels ElGamal génèrent une paire de clés X25519 éphémère pour chaque
saut ECIES dans le tunnel, et utilisent le schéma ci-dessus pour chiffrer leur BuildRequestRecord.
Les créateurs de tunnels ElGamal utiliseront le schéma avant cette spécification pour chiffrer des sauts ElGamal.

Les créateurs de tunnels ECIES devront chiffrer avec la clé publique de chaque saut ElGamal en utilisant le
schéma défini dans [Tunnel-Creation](/en/docs/spec/tunnel-creation/). Les créateurs de tunnels ECIES utiliseront le schéma ci-dessus pour chiffrer
des sauts ECIES.

Cela signifie que les sauts de tunnel verront seulement les enregistrements chiffrés avec leur même type de chiffrement.

Pour les créateurs de tunnels ElGamal et ECIES, ils généreront des paires de clés X25519 éphémères uniques
par saut pour chiffrer des sauts ECIES.

**IMPORTANT**:
Les clés éphémères doivent être uniques par saut ECIES et par enregistrement de construction.
Le fait de ne pas utiliser des clés uniques ouvre une vecteur d'attaque pour des sauts collusoires pour confirmer qu'ils sont dans le même tunnel.


  ```dataspec


// Chaque paire de clés statiques X25519 de saut (hesk, hepk) depuis l'identité du routeur
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || ci-dessous signifie append
  h = SHA256(h || hepk);

  // jusqu'à ici, il peut être précalculé par chaque routeur
  // pour toutes les demandes de construction entrantes

  // L'expéditeur génère une paire de clés éphémères X25519 par saut ECIES dans le VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Fin du modèle de message "e".

  Ceci est le modèle de message "es" :

  // Noise es
  // L'expéditeur effectue un DH X25519 avec la clé publique statique du saut.
  // Chaque saut, trouve l'enregistrement avec leur hash d'identité tronqué,
  // et extrait la clé éphémère de l'expéditeur précédant l'enregistrement encrypté.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Paramètres ChaChaPoly pour chiffrer/déchiffrer
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Sauvegarder pour KDF de l'enregistrement de réponse
  chainKey = keydata[0:31]

  // paramètres AEAD
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Fin du modèle de message "es".

  // MixHash(ciphertext)
  // Sauvegarder pour KDF de l'enregistrement de réponse
  h = SHA256(h || ciphertext)





  ```

``replyKey``, ``layerKey`` et ``layerIV`` doivent encore être incluses dans les enregistrements ElGamal,
et peuvent être générées aléatoirement.


### Chiffrement des enregistrements de demande (ElGamal)

Comme défini dans [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Il n'y a aucun changement à l'encryption pour les sauts ElGamal.




### Chiffrement des enregistrements de réponse (ECIES)

L'enregistrement de réponse est encrypté ChaCha20/Poly1305.

  ```dataspec


// Paramètres AEAD
  k = chainkey de la demande de construction
  n = 0
  plaintext = 512 byte build reply record
  ad = h de la demande de construction

  ciphertext = ENCRYPT(k, n, plaintext, ad)




  ```



### Chiffrement des enregistrements de réponse (ElGamal)

Comme défini dans [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Il n'y a aucun changement à l'encryption pour les sauts ElGamal.



### Analyse de sécurité

ElGamal ne fournit pas de secret en avant pour les messages de construction de tunnel.

AES256/CBC est légèrement en meilleure position, étant seulement vulnérable à un affaiblissement théorique par une
attaque de nœud connu `biclique`.

La seule attaque pratique connue contre l'AES256/CBC est une attaque par oracle de rembourrage, lorsque l'IV est connu de l'attaquant.

Un assaillant devrait casser l'encryption ElGamal du saut suivant pour obtenir les informations de clé AES256/CBC (clé de réponse et IV).

ElGamal est significativement plus intensif pour le CPU qu'ECIES, entraînant une possible épuisement des ressources.

ECIES, utilisé avec de nouvelles clés éphémères par BuildRequestRecord ou VariableTunnelBuildMessage, fournit une secret en avant.

ChaCha20Poly1305 offre un chiffrement AEAD, permettant au destinataire de vérifier l'intégrité du message avant d'essayer de le décrypter.


## Justification

Cette conception maximise la réutilisation des primitives, protocoles et codes cryptographiques existants.
Cette conception minimise le risque.




## Notes de mise en œuvre

* Les anciens routeurs ne vérifient pas le type d'encryption du saut et enverront des enregistrements encryptés ElGamal.
  Certains routeurs récents ont des bugs et enverront divers types d'enregistrements mal formés.
  Les implémenteurs doivent détecter et rejeter ces enregistrements avant l'opération DH
  si possible, pour réduire l'utilisation du CPU.


## Problèmes



## Migration

Voir [Prop156](/en/proposals/156-ecies-routers/).




## Références

.. [Common]
    {{ spec_url('common-structures') }}

.. [Cryptography]
   {{ spec_url('cryptography') }}

.. [ECIES-X25519]
   {{ spec_url('ecies') }}

.. [I2NP]
   {{ spec_url('i2np') }}

.. [NOISE]
    https://noiseprotocol.org/noise.html

.. [NTCP2]
   {{ spec_url('ntcp2') }}

.. [Prop119]
   {{ proposal_url('119') }}

.. [Prop143]
   {{ proposal_url('143') }}

.. [Prop153]
    {{ proposal_url('153') }}

.. [Prop156]
    {{ proposal_url('156') }}

.. [Prop157]
    {{ proposal_url('157') }}

.. [SPEC]
   {{ spec_url('tunnel-creation-ecies') }}

.. [Tunnel-Creation]
   {{ spec_url('tunnel-creation') }}

.. [Multiple-Encryption]
   https://fr.wikipedia.org/wiki/Chiffrement_multiple

.. [RFC-7539]
   https://tools.ietf.org/html/rfc7539

.. [RFC-7748]
   https://tools.ietf.org/html/rfc7748



