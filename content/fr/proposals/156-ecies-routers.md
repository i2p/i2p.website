---
title: "Routeurs ECIES"
number: "156"
author: "zzz, orignal"
created: "2020-09-01"
lastupdated: "2025-03-05"
status: "Fermé"
thread: "http://zzz.i2p/topics/2950"
target: "0.9.51"
toc: true
---

## Remarque
Déploiement et tests réseau en cours.
Sujet à révision.
Statut :

- Routeurs ECIES implémentés depuis la version 0.9.48, voir [Common](/docs/specs/common-structures/).
- Construction de tunnels implémentée depuis la version 0.9.48, voir [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).
- Messages cryptés aux routeurs ECIES implémentés depuis la version 0.9.49, voir [ECIES-ROUTERS](/docs/specs/ecies/).
- Nouveaux messages de construction de tunnels implémentés depuis la version 0.9.51.


## Aperçu


### Résumé

Les identités des routeurs contiennent actuellement une clé de chiffrement ElGamal.
Ceci est la norme depuis les débuts d'I2P.
ElGamal est lent et doit être remplacé partout où il est utilisé.

Les propositions pour LS2 [Prop123](/proposals/123-new-netdb-entries/) et ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
(maintenant spécifiées dans [ECIES](/docs/specs/ecies/)) ont défini le remplacement d'ElGamal par ECIES
pour les destinations.

Cette proposition définit le remplacement d'ElGamal par ECIES-X25519 pour les routeurs.
Cette proposition donne un aperçu des changements nécessaires.
La plupart des détails sont dans d'autres propositions et spécifications.
Voir la section de référence pour les liens.


### Objectifs

Voir [Prop152](/proposals/152-ecies-tunnels/) pour des objectifs supplémentaires.

- Remplacer ElGamal par ECIES-X25519 dans les identités des routeurs
- Réutiliser les primitives cryptographiques existantes
- Améliorer la sécurité des messages de construction de tunnels si possible tout en maintenant la compatibilité
- Prendre en charge les tunnels avec des pairs ElGamal/ECIES mixtes
- Maximiser la compatibilité avec le réseau actuel
- Ne pas nécessiter de mise à niveau « jour J » de l'ensemble du réseau
- Déploiement progressif pour minimiser le risque
- Nouveau message de construction de tunnels plus petit


### Non-Objectifs

Voir [Prop152](/proposals/152-ecies-tunnels/) pour des non-objectifs supplémentaires.

- Pas de nécessité pour des routeurs à double clé
- Changements de chiffrement de couche, pour cela voir [Prop153](/proposals/153-chacha20-layer-encryption/)


## Conception


### Emplacement de la clé et type de crypto

Pour les destinations, la clé est dans le leaseset, pas dans la destination, et
nous prenons en charge plusieurs types de cryptage dans le même leaseset.

Aucun de cela n'est nécessaire pour les routeurs. La clé de chiffrement du routeur
se trouve dans son identité de routeur. Voir la spécification des structures communes [Common](/docs/specs/common-structures/).

Pour les routeurs, nous remplacerons la clé ElGamal de 256 octets dans l'identité du routeur
par une clé X25519 de 32 octets et 224 octets de remplissage.
Ceci sera indiqué par le type de crypto dans le certificat de clé.
Le type de crypto (le même que celui utilisé dans le LS2) est 4.
Cela indique une clé publique X25519 de 32 octets en little-endian.
C'est la construction standard telle que définie dans la spécification des structures communes [Common](/docs/specs/common-structures/).

C'est identique à la méthode proposée pour ECIES-P256
pour les types de cryptos 1-3 dans la proposition 145 [Prop145](/proposals/145-ecies/).
Bien que cette proposition n'ait jamais été adoptée, les développeurs de l'implémentation Java se sont préparés aux
types de cryptos dans les certificats de clé d'identité de routeur en ajoutant des vérifications à plusieurs
endroits dans la base de code. La plupart de ce travail a été effectué à la mi-2019.


### Message de construction de tunnel

Plusieurs changements à la spécification de création de tunnel [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies)
sont nécessaires pour utiliser ECIES au lieu d'ElGamal.
De plus, nous apporterons des améliorations aux messages de construction de tunnel
pour accroître la sécurité.

Dans la phase 1, nous changerons le format et le chiffrement du
Record de demande de construction et du Record de réponse de construction pour les sauts ECIES.
Ces changements seront compatibles avec les routeurs ElGamal existants.
Ces changements sont définis dans la proposition 152 [Prop152](/proposals/152-ecies-tunnels/).

Dans la phase 2, nous ajouterons une nouvelle version du
Message de demande de construction, Message de réponse de construction,
Record de demande de construction, et Record de réponse de construction.
La taille sera réduite pour plus d'efficacité.
Ces changements doivent être pris en charge par tous les sauts dans un tunnel, et tous les sauts doivent être ECIES.
Ces changements sont définis dans la proposition 157 [Prop157](/proposals/157-new-tbm/).


### Chiffrement de bout en bout

#### Historique

Dans la conception originale de Java I2P, il y avait un seul gestionnaire de clé de session ElGamal (SKM)
partagé par le routeur et toutes ses destinations locales.
Comme un SKM partagé pouvait fuir des informations et permettre une corrélation par des attaquants,
la conception a été modifiée pour prendre en charge des SKM ElGamal séparés pour le routeur et chaque destination.
Le design ElGamal ne supportait que les expéditeurs anonymes ;
l'expéditeur envoyait uniquement des clés éphémères, pas de clé statique.
Le message n'était pas lié à l'identité de l'expéditeur.

Ensuite, nous avons conçu le SKM à cliquet ECIES dans
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/), maintenant spécifié dans [ECIES](/docs/specs/ecies/).
Cette conception était spécifiée en utilisant le modèle Noise "IK", qui incluait la clé
statique de l'expéditeur dans le premier message. Ce protocole est utilisé pour les destinations (type 4) ECIES.
Le modèle IK ne permet pas des expéditeurs anonymes.

Par conséquent, nous avons inclus dans la proposition un moyen d'envoyer également des messages anonymes
à un SKM à cliquet, en utilisant une clé statique remplie de zéros. Cela simulait un modèle Noise "N",
mais de manière compatible, afin qu'un SKM ECIES puisse recevoir à la fois des messages anonymes et non anonymes.
L'intention était d'utiliser une clé zéro pour les routeurs ECIES.


#### Cas d'utilisation et modèles de menace

Le cas d'utilisation et le modèle de menace pour les messages envoyés aux routeurs sont très différents de
ceux pour les messages de bout en bout entre destinations.


Cas d'utilisation et modèle de menace de la destination :

- Non-anonyme depuis/vers des destinations (l'expéditeur inclut une clé statique)
- Prise en charge efficace du trafic soutenu entre destinations (poignée de main complète, streaming et tags)
- Toujours envoyé via des tunnels sortants et entrants
- Cacher toutes les caractéristiques identifiantes de l'EPB et de l'IGW, nécessitant un encodage Elligator2 des clés éphémères.
- Les deux participants doivent utiliser le même type de chiffrement


Cas d'utilisation et modèle de menace pour les routeurs :

- Messages anonymes depuis des routeurs ou des destinations (l'expéditeur n'inclut pas de clé statique)
- Pour les recherches et stockages de bases de données cryptées uniquement, généralement inondés
- Messages occasionnels
- Plusieurs messages ne doivent pas être corrélés
- Toujours envoyé via un tunnel sortant directement à un routeur. Aucun tunnel entrant utilisé
- L'OBEP sait qu'il transfère le message à un routeur et connaît son type de chiffrement
- Les deux participants peuvent avoir des types de chiffrement différents
- Les réponses de recherche de base de données sont des messages à usage unique utilisant la clé de réponse et le tag dans le message de recherche de base de données
- Les confirmations de stockage de base de données sont des messages à usage unique utilisant un message d'état de livraison intégré


Objectifs non-visés du cas d'utilisation des routeurs :

- Pas besoin de messages non anonymes
- Pas besoin d'envoyer des messages via des tunnels exploratoires entrants (un routeur ne publie pas de leasesets exploratoires)
- Pas besoin de trafic soutenu de messages utilisant des tags
- Pas besoin d'exécuter des gestionnaires de clés de session "à double clé" comme décrit dans [ECIES](/docs/specs/ecies/) pour les destinations. Les routeurs n'ont qu'une seule clé publique.


#### Conclusion de la conception

Le SKM de routeur ECIES n'a pas besoin d'un SKM à cliquet complet tel que spécifié dans [ECIES](/docs/specs/ecies/) pour les destinations.
Il n'y a pas de besoin de messages non-anonymes utilisant le modèle IK.
Le modèle de menace ne nécessite pas de clés éphémères encodées Elligator2.

Par conséquent, le SKM du routeur utilisera le modèle Noise "N", le même que spécifié
dans [Prop152](/proposals/152-ecies-tunnels/) pour la construction de tunnels.
Il utilisera le même format de charge utile que spécifié dans [ECIES](/docs/specs/ecies/) pour les destinations.
Le mode à clé statique zéro (pas de liaison ou session) de IK spécifié dans [ECIES](/docs/specs/ecies/) ne sera pas utilisé.

Les réponses aux recherches seront chiffrées avec un tag à cliquet si demandé dans la recherche.
C'est comme documenté dans [Prop154](/proposals/154-ecies-lookups/), maintenant spécifié dans [I2NP](/docs/specs/i2np/).

La conception permet au routeur d'avoir un seul gestionnaire de clé de session ECIES.
Il n'est pas nécessaire d'exécuter des gestionnaires de clés de session "à double clé" tel que
décrit dans [ECIES](/docs/specs/ecies/) pour les destinations.
Les routeurs n'ont qu'une seule clé publique.

Un routeur ECIES n'a pas de clé statique ElGamal.
Le routeur a encore besoin d'une implémentation d'ElGamal pour construire des tunnels
à travers des routeurs ElGamal et envoyer des messages chiffrés à des routeurs ElGamal.

Un routeur ECIES PEUT nécessiter un gestionnaire de clé de session partiel ElGamal pour
recevoir des messages marqués ElGamal reçus en tant que réponses aux recherches NetDB
des routeurs floodfill antérieurs à la version 0.9.46, car ces routeurs n'ont pas
une implémentation de réponses marquées ECIES tel que spécifié dans [Prop152](/proposals/152-ecies-tunnels/).
Sinon, un routeur ECIES ne peut pas demander une réponse cryptée d'un
routeur floodfill antérieur à la version 0.9.46.

C'est optionnel. La décision peut varier dans différentes implémentations I2P
et peut dépendre de la portion du réseau ayant été mise à niveau vers
0.9.46 ou version ultérieure.
À ce jour, environ 85 % du réseau est en version 0.9.46 ou supérieure.


## Spécification

X25519 : Voir [ECIES](/docs/specs/ecies/).

Identité de routeur et certificat de clé : Voir [Common](/docs/specs/common-structures/).

Construction de tunnels : Voir [Prop152](/proposals/152-ecies-tunnels/).

Nouveau message de construction de tunnels : Voir [Prop157](/proposals/157-new-tbm/).


### Chiffrement des requêtes

Le chiffrement des demandes est le même que celui spécifié dans [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) et [Prop152](/proposals/152-ecies-tunnels/),
utilisant le modèle Noise "N".

Les réponses aux recherches seront chiffrées avec un tag à cliquet si demandé dans la recherche.
Les messages de demande de recherche de base de données contiennent la clé de réponse de 32 octets et le tag de réponse de 8 octets
tels que spécifiés dans [I2NP](/docs/specs/i2np/) et [Prop154](/proposals/154-ecies-lookups/). La clé et le tag sont utilisés pour chiffrer la réponse.

Les ensembles de tags ne sont pas créés.
Le schéma à clé statique zéro spécifié dans
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) et [ECIES](/docs/specs/ecies/) ne sera pas utilisé.
Les clés éphémères ne seront pas encodées en Elligator2.

En général, ce seront des messages de nouvelle session et seront envoyés avec une clé statique zéro
(pas de liaison ou session), car l'expéditeur du message est anonyme.


#### KDF pour ck et h initiaux

Cela fait partie du standard [NOISE](https://noiseprotocol.org/noise.html) pour le modèle "N" avec un nom de protocole standard.
C'est le même que spécifié dans [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) et [Prop152](/proposals/152-ecies-tunnels/) pour les messages de construction de tunnel.


  ```text

C'est le modèle de message "e" :

  // Définir protocol_name.
  Définir protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 octets, US-ASCII encodé, sans terminaison NULL).

  // Définir Hash h = 32 octets
  // Remplir pour atteindre 32 octets. NE PAS le hacher, car il ne fait pas plus de 32 octets.
  h = protocol_name || 0

  Définir ck = clé de chaînage de 32 octets. Copier les données de h dans ck.
  Définir chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // jusqu'ici, tout peut être précalculé par tous les routeurs.


  ```


#### KDF pour les messages

Les créateurs de message génèrent une paire de clés éphémères X25519 pour chaque message.
Les clés éphémères doivent être uniques par message.
C'est le même que spécifié dans [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) et [Prop152](/proposals/152-ecies-tunnels/) pour les messages de construction de tunnel.


  ```dataspec


// Clé statique de l'itinéraire cible X25519 (hesk, hepk) de l'identité du routeur
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || ci-dessous veut dire ajouter
  h = SHA256(h || hepk);

  // jusqu'ici, tout peut être précalculé par chaque routeur
  // pour tous les messages entrants

  // L'expéditeur génère une paire de clés éphémères X25519
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Fin du modèle de message "e".

  C'est le modèle de message "es" :

  // Noise es
  // L'expéditeur effectue un DH X25519 avec la clé publique statique du récepteur.
  // Le routeur cible
  // extrait la clé éphémère de l'expéditeur précédant l'enregistrement chiffré.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Paramètres ChaChaPoly pour chiffrer/décrypter
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // La clé de chaîne n'est pas utilisée
  //chainKey = keydata[0:31]

  // Paramètres AEAD
  k = keydata[32:63]
  n = 0
  plaintext = enregistrement de demande de construction de 464 octets
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Fin du modèle de message "es".

  // MixHash(ciphertext) n'est pas requis
  //h = SHA256(h || ciphertext)


  ```


#### Charge utile

La charge utile est le même format de bloc que défini dans [ECIES](/docs/specs/ecies/) et [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Tous les messages doivent contenir un bloc DateTime pour la prévention de la relecture.


### Chiffrement des réponses

Les réponses aux messages de recherche de base de données sont des messages de stockage de base de données ou de réponse de recherche de base de données.
Ils sont chiffrés en tant que messages de session existants avec
la clé de réponse de 32 octets et le tag de réponse de 8 octets
tel que spécifié dans [I2NP](/docs/specs/i2np/) et [Prop154](/proposals/154-ecies-lookups/).


Il n'y a pas de réponses explicites aux messages de stockage de base de données. L'expéditeur peut intégrer sa
propre réponse sous forme de message Garlic à lui-même, contenant un message d'état de livraison.


## Justification

Cette conception maximise la réutilisation des primitives cryptographiques existantes, des protocoles et du code.

Cette conception minimise le risque.


## Notes d'implémentation

Les anciens routeurs ne vérifient pas le type de chiffrement du routeur et enverront des enregistrements de construction ou des messages netdb chiffrés avec ElGamal.
Certains routeurs récents sont bogués et enverront différents types d'enregistrements de construction malformés.
Certains routeurs récents peuvent envoyer des messages netdb non-anonymes (cliquet complet).
Les implémenteurs devraient détecter et rejeter ces enregistrements et messages
dès que possible, pour réduire l'utilisation du processeur.


## Problèmes

La proposition 145 [Prop145](/proposals/145-ecies/) pourrait ou non être réécrite pour être principalement compatible avec
la proposition 152 [Prop152](/proposals/152-ecies-tunnels/).


## Migration

L'implémentation, les tests et le déploiement s'étaleront sur plusieurs versions
et environ un an. Les phases sont les suivantes. L'attribution de
chaque phase à une version particulière est à déterminer et dépend du
rythme de développement.

Les détails de l'implémentation et de la migration peuvent varier pour
chaque implémentation I2P.


### Point à point de base

Les routeurs ECIES peuvent se connecter et recevoir des connexions des routeurs ElGamal.
Cela devrait être possible maintenant, car plusieurs vérifications ont été ajoutées à la base de code Java
à la mi-2019 en réaction à la proposition 145 [Prop145](/proposals/145-ecies/) inachevée.
Veillez à ce qu'il n'y ait rien dans les bases de code
qui empêche les connexions point à point vers des routeurs non-ElGamal.

Contrôles de conformité du code :

- S'assurer que les routeurs ElGamal ne demandent pas de réponses chiffrées AEAD aux messages de recherche de base de données
  (quand la réponse revient par un tunnel exploratoire vers le routeur)
- S'assurer que les routeurs ECIES ne demandent pas de réponses chiffrées AES aux messages de recherche de base de données
  (quand la réponse revient par un tunnel exploratoire vers le routeur)

Jusqu'à des phases ultérieures, lorsque les spécifications et les implémentations seront complètes :

- S'assurer que la construction de tunnels n'est pas tenté par des routeurs ElGamal à travers des routeurs ECIES.
- S'assurer que des messages chiffrés ElGamal ne sont pas envoyés par des routeurs ElGamal aux routeurs ECIES floodfill.
  (Recherches de base de données et Stockages de base de données)
- S'assurer que des messages chiffrés ECIES ne sont pas envoyés par des routeurs ECIES aux routeurs ElGamal floodfill.
  (Recherches de base de données et Stockages de base de données)
- S'assurer que les routeurs ECIES ne deviennent pas automatiquement floodfill.

Aucune modification ne devrait être requise.
Version cible, si des modifications sont nécessaires : 0.9.48


### Compatibilité NetDB

Assurez-vous que les infos de routeur ECIES puissent être stockées et récupérées à partir des floodfills ElGamal.
Cela devrait être possible maintenant, car plusieurs vérifications ont été ajoutées à la base de code Java
à la mi-2019 en réaction à la proposition 145 [Prop145](/proposals/145-ecies/) inachevée.
Assurez-vous qu'il n'y a rien dans les bases de code
qui empêche le stockage d'info de routeur non-ElGamal dans la base de données du réseau.

Aucune modification ne devrait être requise.
Version cible, si des modifications sont nécessaires : 0.9.48


### Construction de tunnel

Implémentez la construction de tunnel telle que définie dans la proposition 152 [Prop152](/proposals/152-ecies-tunnels/).
Commencez par faire construire aux routeurs ECIES des tunnels avec tous les sauts ElGamal ;
utilisez leur propre enregistrement de demande de construction pour un tunnel entrant à tester et déboguer.

Ensuite, testerez et supportez les routeurs ECIES construisant des tunnels avec un mélange de
sauts ElGamal et ECIES.

Ensuite, autorisez la construction de tunnels à travers les routeurs ECIES.
Aucun contrôle de version minimum ne devrait être nécessaire à moins que des changements incompatibles
à la proposition 152 ne soient apportés après une version.

Version cible : 0.9.48, fin 2020


### Messages à cliquet aux floodfills ECIES

Implémentez et testez la réception des messages ECIES (avec clé statique zéro) par les floodfills ECIES,
tels que définis dans la proposition 144 [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Implémentez et testez la réception des réponses chiffrées AEAD aux messages de recherche de base de données par les routeurs ECIES.

Activez l'auto-floodfill par les routeurs ECIES.
Ensuite, permettez l'envoi de messages ECIES aux routeurs ECIES.
Aucun contrôle de version minimum ne devrait être nécessaire à moins que des changements incompatibles
à la proposition 152 ne soient apportés après une version.

Version cible : 0.9.49, début 2021.
Les routeurs ECIES peuvent automatiquement devenir floodfill.


### Changement de clé et nouvelles installations

Les nouvelles installations par défaut utiliseront ECIES à partir de la version 0.9.49.

Reconfigurez progressivement tous les routeurs pour minimiser le risque et la perturbation du réseau.
Utilisez le code existant qui a effectué le changement de clé pour la migration du type de signature il y a des années.
Ce code donne à chaque routeur une petite chance aléatoire de reconfigurer sa clé à chaque redémarrage.
Après plusieurs redémarrages, un routeur aura probablement reconfiguré sa clé vers ECIES.

Le critère pour commencer le changement de clé est qu'une portion suffisante du réseau,
peut-être 50 %, puisse construire des tunnels à travers des routeurs ECIES (0.9.48 ou version ultérieure).

Avant de changer agressivement la clé de l'ensemble du réseau, la grande majorité
(peut-être 90 % ou plus) doit être capable de construire des tunnels à travers des routeurs ECIES (0.9.48 ou version ultérieure)
ET d'envoyer des messages aux floodfills ECIES (0.9.49 ou version ultérieure).
Cet objectif sera probablement atteint pour la version 0.9.52.

Le changement de clé prendra plusieurs versions.

Version cible :
0.9.49 pour que les nouveaux routeurs par défaut utilisent ECIES ;
0.9.49 pour commencer lentement le changement de clé ;
0.9.50 - 0.9.52 pour augmenter progressivement le taux de changement de clé ;
fin 2021 pour que la majorité du réseau soit reconfigurée.


### Nouveau message de construction de tunnel (Phase 2)

Implémentez et testez le nouveau message de construction de tunnel tel que défini dans la proposition 157 [Prop157](/proposals/157-new-tbm/).
Déployer la prise en charge dans la version 0.9.51.
Faire des tests supplémentaires, puis activer dans la version 0.9.52.

Les tests seront difficiles.
Avant que cela puisse être largement testé, une bonne partie du réseau doit le prendre en charge.
Avant que ce soit largement utile, la majorité du réseau doit le prendre en charge.
Si des modifications de spécification ou d'implémentation sont nécessaires après les tests,
cela retarderait le déploiement d'une version supplémentaire.

Version cible : 0.9.52, fin 2021.


### Changement de clé complet

À ce stade, les routeurs plus anciens qu'une version TBD ne
pourront pas construire des tunnels à travers la plupart des pairs.

Version cible : 0.9.53, début 2022.


## Références

* [Common](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [ECIES-ROUTERS](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
* [Prop145](/proposals/145-ecies/)
* [Prop152](/proposals/152-ecies-tunnels/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop154](/proposals/154-ecies-lookups/)
* [Prop157](/proposals/157-new-tbm/)
* [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies)
* [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
