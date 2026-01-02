---
title: "Paramètres de Bande Passante du Tunnel"
number: "168"
author: "zzz"
created: "2024-07-31"
lastupdated: "2024-12-10"
status: "Fermé"
thread: "http://zzz.i2p/topics/3652"
target: "0.9.65"
toc: true
---

## REMARQUE

Cette proposition a été approuvée et est maintenant incluse dans la
[Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies) depuis l'API 0.9.65.
Il n'existe aucune implémentation connue pour le moment; les dates d'implémentation / versions de l'API sont à déterminer.


## Aperçu

Au fur et à mesure que nous avons augmenté les performances du réseau au cours des dernières années
avec de nouveaux protocoles, types de chiffrement et améliorations du contrôle de congestion,
des applications plus rapides telles que le streaming vidéo deviennent possibles.
Ces applications nécessitent une bande passante élevée à chaque saut dans leurs tunnels clients.

Cependant, les routeurs participants ne disposent d'aucune information sur la quantité
de bande passante qu'un tunnel utilisera lorsqu'ils reçoivent un message de construction de tunnel.
Ils ne peuvent accepter ou refuser un tunnel qu'en fonction de la bande passante totale
actuellement utilisée par tous les tunnels participants et de la limite totale de bande passante pour les tunnels participants.

Les routeurs demandeurs n'ont également aucune information sur la quantité de bande passante
disponible à chaque saut.

De plus, les routeurs n'ont actuellement aucun moyen de limiter le trafic entrant sur un tunnel.
Cela serait très utile en cas de surcharge ou d'attaque DDoS d'un service.

Cette proposition aborde ces problèmes en ajoutant des paramètres de bande passante aux
messages de demande et de réponse de construction de tunnel.


## Conception

Ajouter des paramètres de bande passante aux enregistrements dans les messages de construction de tunnel ECIES (voir [Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies))
dans le champ de mappage des options de construction de tunnel. Utiliser des noms de paramètres courts puisque l'espace disponible
pour le champ des options est limité.
Les messages de construction de tunnel sont de taille fixe, donc cela n'augmente pas la
taille des messages.


## Spécification

Mettre à jour la [spécification du message de construction de tunnel ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
comme suit :

Pour les enregistrements de construction ECIES longs et courts :

### Options de Demande de Construction

Les trois options suivantes peuvent être définies dans le champ de mappage des options de construction de tunnel de l'enregistrement :
Un routeur demandeur peut inclure n'importe quelle(s), toutes, ou aucune.

- m := bande passante minimum requise pour ce tunnel (entier positif en Ko/s sous forme de chaîne)
- r := bande passante demandée pour ce tunnel (entier positif en Ko/s sous forme de chaîne)
- l := limiter la bande passante pour ce tunnel ; envoyé uniquement à IBGW (entier positif en Ko/s sous forme de chaîne)

Contrainte : m <= r <= l

Le routeur participant devrait refuser le tunnel si "m" est spécifié et qu'il ne peut pas
fournir au moins cette bande passante.

Les options de demande sont envoyées à chaque participant dans l'enregistrement de demande de construction crypté correspondant,
et ne sont pas visibles pour les autres participants.


### Option de Réponse de Construction

L'option suivante peut être définie dans le champ de mappage des options de réponse de construction du tunnel de l'enregistrement,
lorsque la réponse est ACCEPTÉE :

- b := bande passante disponible pour ce tunnel (entier positif en Ko/s sous forme de chaîne)

Le routeur participant devrait inclure cela si "m" ou "r" a été spécifié
dans la demande de construction. La valeur doit être au moins égale à celle de la valeur "m" si spécifiée,
mais peut être inférieure ou supérieure à la valeur "r" si spécifiée.

Le routeur participant devrait tenter de réserver et de fournir au moins cette
quantité de bande passante pour le tunnel, cependant cela n'est pas garanti.
Les routeurs ne peuvent pas prévoir les conditions 10 minutes à l'avance, et
le trafic participant est de priorité inférieure à celui du trafic et des tunnels propres au routeur.

Les routeurs peuvent également sur-allouer la bande passante disponible si nécessaire, et cela est
probablement souhaitable, car d'autres sauts dans le tunnel pourraient le rejeter.

Pour ces raisons, la réponse du routeur participant devrait être traitée
comme un engagement de meilleure-effort, mais pas une garantie.

Les options de réponse sont envoyées au routeur demandeur dans l'enregistrement de réponse de construction crypté correspondant,
et ne sont pas visibles pour les autres participants.


## Notes d'Implémentation

Les paramètres de bande passante sont tels qu'ils sont vus aux routeurs participants au niveau du tunnel,
c'est-à-dire le nombre de messages de tunnel de 1 Ko de taille fixe par seconde.
La surcharge de transport (NTCP2 ou SSU2) n'est pas incluse.

Cette bande passante peut être bien plus ou moins que la bande passante vue au niveau du client.
Les messages de tunnel contiennent une surcharge substantielle, y compris la surcharge des couches supérieures
incluant le décrochage et le streaming. Les messages intermittents petits tels que les acquittements de streaming
seront étendus à 1 Ko chacun.
Cependant, la compression gzip au niveau I2CP peut réduire considérablement la bande passante.

La mise en œuvre la plus simple au niveau du routeur demandeur est d'utiliser
les bandes passantes moyennes, minimales et/ou maximales des tunnels actuels dans le pool
pour calculer les valeurs à mettre dans la demande.
Des algorithmes plus complexes sont possibles et sont à la discrétion de l'implémenteur.

Il n'existe actuellement aucune option I2CP ou SAM définie pour que le client indique au
routeur quelle bande passante est requise, et aucune nouvelle option n'est proposée ici.
Les options peuvent être définies ultérieurement si nécessaire.

Les implémentations peuvent utiliser la bande passante disponible ou toutes autres données, algorithmes, politiques locales,
ou configurations locales pour calculer la valeur de bande passante retournée dans la
réponse de construction. Non spécifié par cette proposition.

Cette proposition nécessite que les passerelles entrantes mettent en œuvre un
throttling par tunnel si demandé par l'option "l".
Elle n'exige pas que les autres sauts participants mettent en œuvre un throttling par tunnel ou global
de tout type, ou spécifient un algorithme ou une implémentation particulière, le cas échéant.

Cette proposition n'exige pas non plus que les routeurs clients limitent le trafic
à la valeur "b" retournée par le saut participant, et selon l'application,
cela pourrait ne pas être possible, en particulier pour les tunnels entrants.

Cette proposition ne concerne que les tunnels créés par l'initiateur. Aucune
méthode n'est définie pour demander ou allouer une bande passante pour des tunnels "à l'autre extrémité" créés
par le propriétaire de l'autre extrémité d'une connexion de bout en bout.


## Analyse de Sécurité

La prise d'empreinte client ou la corrélation peut être possible en fonction des demandes.
Le routeur client (initial) peut souhaiter randomiser les valeurs "m" et "r" plutôt que d'envoyer
la même valeur à chaque saut; ou envoyer un ensemble limité de valeurs représentant des "seaux" de bande passante,
ou une combinaison des deux.

Sur-allocation DDoS : Bien qu'il soit possible actuellement de mener une attaque DDoS sur un routeur en construisant et en
utilisant un grand nombre de tunnels à travers lui, cette proposition rend probablement cela plus facile,
en demandant simplement un ou plusieurs tunnels avec de grandes demandes de bande passante.

Les implémentations peuvent et devraient utiliser une ou plusieurs des stratégies suivantes
pour atténuer ce risque :

- Sur-allocation de la bande passante disponible
- Limiter l'allocation par tunnel à un certain pourcentage de la bande passante disponible
- Limiter le taux d'augmentation de la bande passante allouée
- Limiter le taux d'augmentation de la bande passante utilisée
- Limiter la bande passante allouée pour un tunnel si elle n'est pas utilisée tôt dans la durée de vie du tunnel (utilisez-la ou perdez-la)
- Suivre la bande passante moyenne par tunnel
- Suivre la bande passante demandée vs. vraiment utilisée par tunnel


## Compatibilité

Aucun problème. Toutes les mises en œuvre connues ignorent actuellement le champ de mappage dans les messages de construction,
et passent correctement sur un champ d'options non vide.


## Migration

Les implémentations peuvent ajouter le support à tout moment, aucune coordination n'est nécessaire.

Puisqu'il n'existe actuellement aucune version d'API définie où le support pour cette proposition est requis,
les routeurs devraient vérifier une réponse "b" pour confirmer le support.


