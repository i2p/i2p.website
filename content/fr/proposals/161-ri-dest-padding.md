---
title: "RI et Remplissage de Destination"
number: "161"
author: "zzz"
created: "2022-09-28"
lastupdated: "2023-01-02"
status: "Open"
thread: "http://zzz.i2p/topics/3279"
target: "0.9.57"
toc: true
---

## Statut

Implémenté dans la version 0.9.57.
Laisser cette proposition ouverte afin que nous puissions améliorer et discuter des idées dans la section "Planification future".


## Aperçu


### Résumé

La clé publique ElGamal dans les Destinations n'a pas été utilisée depuis la version 0.6 (2005).
Bien que nos spécifications indiquent qu'elle est inutilisée, elles NE disent PAS que les implémentations peuvent éviter
de générer une paire de clés ElGamal et simplement remplir le champ avec des données aléatoires.

Nous proposons de modifier les spécifications pour indiquer que
le champ est ignoré et que les implémentations PEUVENT remplir le champ avec des données aléatoires.
Ce changement est rétrocompatible. Il n'existe aucune implémentation connue qui valide
la clé publique ElGamal.

De plus, cette proposition offre des conseils aux développeurs sur la façon de générer
les données aléatoires pour le remplissage de l'Identité de Destination ET du Routeur afin qu'elles soient compressibles tout en
restant sécurisées, et sans que les représentations en Base 64 ne paraissent corrompues ou non sécurisées.
Cela fournit la plupart des avantages de la suppression des champs de remplissage sans
aucun changement perturbateur du protocole.
Les Destinations compressibles réduisent la taille du SYN en streaming et des datagrammes à réponse ;
les Identités de Routeur compressibles réduisent la taille des Messages de Stockage de Base de Données, des messages SSU2 Session Confirmed,
et des fichiers su3 de resemance.

Enfin, la proposition discute des possibilités de nouveaux formats de Destination et d'Identité de Routeur
qui élimineraient complètement le remplissage. Il y a également une brève discussion sur la cryptographie post-quantique
et comment cela pourrait affecter la planification future.



### Objectifs

- Éliminer l'obligation de générer une paire de clés ElGamal pour les Destinations
- Recommander les meilleures pratiques pour que les Destinations et les Identités de Routeur soient hautement compressibles,
  tout en n'affichant pas de motifs évidents dans les représentations en Base 64.
- Encourager l'adoption des meilleures pratiques par toutes les implémentations pour que
  les champs ne soient pas distinguables
- Réduire la taille du SYN en streaming
- Réduire la taille des datagrammes à réponse
- Réduire la taille du bloc RI SSU2
- Réduire la taille du SSU2 Session Confirmed et la fréquence de fragmentation
- Réduire la taille des Messages de Stockage de Base de Données (avec RI)
- Réduire la taille des fichiers de resemance
- Maintenir la compatibilité dans tous les protocoles et APIs
- Mettre à jour les spécifications
- Discuter des alternatives pour de nouveaux formats de Destination et d'Identité de Routeur

En éliminant l'exigence de générer des clés ElGamal, les implémentations pourraient
être en mesure de supprimer complètement le code ElGamal, sous réserve de considérations de rétrocompatibilité
dans d'autres protocoles.



## Conception

À proprement parler, la clé publique de signature de 32 octets seule (dans les Destinations et les Identités de Routeur)
et la clé publique de chiffrement de 32 octets (uniquement dans les Identités de Routeur) est un nombre aléatoire
qui fournit toute l'entropie nécessaire pour que les hachages SHA-256 de ces structures
soient cryptographiquement forts et distribués aléatoirement dans la base de données en réseau DHT.

Cependant, par précaution, nous recommandons d'utiliser un minimum de 32 octets de données aléatoires
dans le champ de clé publique ElG et le remplissage. De plus, si les champs étaient tous des zéros,
les destinations en Base 64 contiendraient de longues séquences de caractères AAAA, ce qui pourrait
alarmer ou confondre les utilisateurs.

Pour le type de signature Ed25519 et le type de chiffrement X25519 :
Les Destinations contiendront 11 copies (352 octets) des données aléatoires.
Les Identités de Routeur contiendront 10 copies (320 octets) des données aléatoires.



### Économies Estimées

Les Destinations sont incluses dans chaque SYN en streaming
et datagramme à réponse.
Les Infos Routeur (contenant des Identités de Routeur) sont incluses dans les Messages de Stockage de Base de Données
et dans les messages Session Confirmed dans NTCP2 et SSU2.

NTCP2 ne compresse pas l'Info Routeur.
Les RIs dans les Messages de Stockage de Base de Données et les messages SSU2 Session Confirmed sont compressés avec gzip.
Les Infos Routeur sont comprimées dans les fichiers SU3 de resemance.

Les Destinations dans les Messages de Stockage de Base de Données ne sont pas compressées.
Les messages SYN en streaming sont compressés avec gzip au niveau de l'I2CP.

Pour le type de signature Ed25519 et le type de chiffrement X25519,
économies estimées :

| Type de Données | Taille Totale | Clés et Cert | Remplissage Non-Comprimé | Remplissage Compressé | Taille | Économies |
|-----------------|---------------|--------------|--------------------------|----------------------|--------|-----------|
| Destination | 391 | 39 | 352 | 32 | 71 | 320 octets (82%) |
| Identité Routeur | 391 | 71 | 320 | 32 | 103 | 288 octets (74%) |
| Info Routeur | 1000 typ. | 71 | 320 | 32 | 722 typ. | 288 octets (29%) |

Notes : Suppose qu'un certificat de 7 octets n'est pas compressible, aucune surcharge gzip supplémentaire.
Aucun des deux n'est vrai, mais les effets seront faibles.
Ignore d'autres parties compressibles de l'Info Routeur.



## Spécification

Les changements proposés à nos spécifications actuelles sont documentés ci-dessous.


### Structures Communes
Modifier la spécification des structures communes
pour spécifier que le champ de clé publique de 256 octets de la Destination est ignoré et peut
contenir des données aléatoires.

Ajouter une section à la spécification des structures communes
recommandant les meilleures pratiques pour le champ de clé publique de la Destination et les
champs de remplissage dans la Destination et l'Identité de Routeur, comme suit :

Générez 32 octets de données aléatoires en utilisant un générateur de nombres pseudo-aléatoires cryptographiquement fort (PRNG)
et répétez ces 32 octets autant que nécessaire pour remplir le champ de clé publique (pour les Destinations)
et le champ de remplissage (pour les Destinations et les Identités de Routeur).

### Fichier de Clé Privée
Le format du fichier de clé privée (eepPriv.dat) ne fait pas officiellement partie de nos spécifications
mais il est documenté dans les [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html)
et d'autres implémentations le supportent.
Cela permet la portabilité des clés privées vers différentes implémentations.
Ajoutez une note à ce javadoc que la clé publique de chiffrement peut être un remplissage aléatoire
et que la clé privée de chiffrement peut être composée de zéros ou de données aléatoires.

### SAM
Indiquer dans la spécification SAM que la clé privée de chiffrement n'est pas utilisée et peut être ignorée.
Toutes les données aléatoires peuvent être retournées par le client.
Le SAM Bridge peut envoyer des données aléatoires lors de la création (avec DEST GENERATE ou SESSION CREATE DESTINATION=TRANSIENT)
plutôt que des zéros, afin que la représentation en Base 64 n'ait pas une série de caractères AAAA
et paraisse cassée.


### I2CP
Aucun changement requis pour I2CP. La clé privée pour la clé publique de chiffrement dans la Destination
n'est pas envoyée au routeur.


## Planification Future


### Changements de Protocole

Au coût de changements de protocole et d'un manque de rétrocompatibilité, nous pourrions
modifier nos protocoles et spécifications pour éliminer le champ de remplissage dans
la Destination, l'Identité de Routeur, ou les deux.

Cette proposition a une certaine similitude avec le format de jeux de lease "b33" chiffré,
contenant uniquement une clé et un champ de type.

Pour maintenir une certaine compatibilité, certaines couches de protocole pourraient "étendre" le champ de remplissage
avec des zéros pour les présenter à d'autres couches de protocole.

Pour les Destinations, nous pourrions également supprimer le champ de type de chiffrement dans le certificat de clé,
économisant ainsi deux octets.
Alternativement, les Destinations pourraient recevoir un nouveau type de chiffrement dans le certificat de clé,
indiquant une clé publique zéro (et un remplissage).

Si la conversion de compatibilité entre anciens et nouveaux formats n'est pas incluse à une certaine couche de protocole,
les spécifications, APIs, protocoles, et applications suivants seraient affectés :

- Spécification des structures communes
- I2NP
- I2CP
- NTCP2
- SSU2
- Ratchet
- Streaming
- SAM
- Bittorrent
- Reseeding
- Fichier de Clé Privée
- API cœur Java et routeur
- API i2pd
- Bibliothèques SAM tierces
- Outils intégrés et tiers
- Plusieurs plugins Java
- Interfaces utilisateur
- Applications P2P e.g. MuWire, bitcoin, monero
- hosts.txt, carnet d'adresses et abonnements

Si la conversion est spécifiée à une certaine couche, la liste serait réduite.

Les coûts et bénéfices de ces changements ne sont pas clairs.

Propositions spécifiques à définir :





### Clés PQ

Les clés publiques de chiffrement post-quantique (PQ), pour tout algorithme anticipé,
sont plus grandes que 256 octets. Cela éliminerait tout remplissage et toute économie provenant des changements proposés ci-dessus pour les Identités de Routeur.

Dans une approche PQ "hybride", comme ce que fait SSL, les clés PQ seraient uniquement éphémères,
et n'apparaîtraient pas dans l'Identité de Routeur.

Les clés de signature PQ ne sont pas viables,
et les Destinations ne contiennent pas de clés publiques de chiffrement.
Les clés statiques pour ratchet sont dans le Jeux de Leases, pas dans la Destination.
nous pouvons donc éliminer les Destinations de la discussion suivante.

Donc PQ n'affecte que les Infos Routeur, et uniquement pour les clés statiques PQ (pas éphémères), pas pour le PQ hybride.
Cela serait pour un nouveau type de chiffrement et affecterait NTCP2, SSU2, et
les Messages de Recherche de Base de Données chiffrés et leurs réponses.
Délai estimé pour la conception, le développement, et le déploiement de cela serait ????????
Mais serait après hybride ou ratchet ????????????

Pour de plus amples discussions, voir [this topic](http://zzz.i2p/topics/3294).




## Problèmes

Il pourrait être souhaitable de changer les clés du réseau à un rythme lent, pour fournir une couverture aux nouveaux routeurs.
"Rekeying" pourrait signifier simplement changer le remplissage, pas vraiment changer les clés.

Il n'est pas possible de changer les clés des Destinations existantes.

Les Identités de Routeur avec remplissage dans le champ de clé publique devraient-elles être identifiées avec un type de chiffrement différent dans le certificat de clé ? Cela entraînerait des problèmes de compatibilité.




## Migration

Aucun problème de rétrocompatibilité pour remplacer la clé ElGamal par du remplissage.

Changer les clés, si mis en œuvre, serait similaire à ce qui a été fait
dans trois transitions d'identité de routeur précédentes :
de DSA-SHA1 à ECDSA, puis à
EdDSA, puis à X25519.

Sous réserve de questions de rétrocompatibilité, et après avoir désactivé SSU,
les implémentations peuvent supprimer complètement le code ElGamal.
Environ 14 % des routeurs du réseau sont de type de chiffrement ElGamal, y compris de nombreux floodfills.

Une demande de fusion brouillon pour Java I2P est disponible à [git.idk.i2p](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/merge_requests/66).
