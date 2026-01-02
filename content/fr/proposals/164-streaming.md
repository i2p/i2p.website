---
title: "Mises à jour de Streaming"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Fermé"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## Vue d'ensemble

Les routeurs Java I2P et i2pd antérieurs à l'API 0.9.58 (publiée en mars 2023)
sont vulnérables à une attaque de relecture de paquets SYN en streaming.
Il s'agit d'un problème de conception de protocole, pas d'un bug d'implémentation.

Les paquets SYN sont signés, mais la signature du paquet SYN initial envoyé d'Alice à Bob
n'est pas liée à l'identité de Bob, donc Bob peut stocker et rejouer ce paquet,
l'envoyant à une victime Charlie. Charlie pensera que le paquet vient
d'Alice et lui répondra. Dans la plupart des cas, ceci est inoffensif, mais
le paquet SYN peut contenir des données initiales (comme un GET ou un POST) que
Charlie traitera immédiatement.


## Conception

La solution consiste pour Alice à inclure le hash de destination de Bob dans les données SYN signées.
Bob vérifie à la réception que ce hash correspond à son hash.

Toute éventuelle victime d'attaque Charlie
vérifie cette donnée et rejette le SYN si elle ne correspond pas à son hash.

En utilisant le champ d'option NACKs dans le SYN pour stocker le hash,
le changement est rétrocompatible, car les NACKs ne sont pas censés être inclus
dans le paquet SYN et sont actuellement ignorés.

Toutes les options sont couvertes par la signature, comme d'habitude, donc Bob ne peut pas
réécrire le hash.

Si Alice et Charlie disposent de l'API 0.9.58 ou plus récent, toute tentative de relecture par Bob sera rejetée.


## Spécification

Mettre à jour la [spécification Streaming](/docs/specs/streaming/) pour ajouter la section suivante :

### Prévention de la relecture

Pour empêcher Bob d'utiliser une attaque de relecture en stockant un paquet SYNCHRONIZE signé valide
reçu d'Alice et en l'envoyant plus tard à une victime Charlie,
Alice doit inclure le hash de destination de Bob dans le paquet SYNCHRONIZE comme suit :

.. raw:: html

  {% highlight lang='dataspec' %}
Set NACK count field to 8
  Set the NACKs field to Bob's 32-byte destination hash

{% endhighlight %}

À la réception d'un SYNCHRONIZE, si le champ de comptage NACK est 8,
Bob doit interpréter le champ NACKs comme un hash de destination de 32 octets,
et doit vérifier qu'il correspond à son hash de destination.
Il doit aussi vérifier la signature du paquet comme d'habitude,
car cela couvre l'ensemble du paquet y compris les champs de comptage NACK et NACKs.
Si le comptage NACK est 8 et que le champ NACKs ne correspond pas,
Bob doit ignorer le paquet.

Ceci est requis pour les versions 0.9.58 et supérieures.
Ceci est rétrocompatible avec les versions antérieures,
car les NACKs ne sont pas attendus dans un paquet SYNCHRONIZE.
Les destinations ne peuvent pas savoir quelle version l'autre extrémité utilise.

Aucun changement n'est nécessaire pour le paquet SYNCHRONIZE ACK envoyé de Bob à Alice ;
ne pas inclure les NACKs dans ce paquet.


## Analyse de sécurité

Ce problème est présent dans le protocole de streaming depuis sa création en 2004.
Il a été découvert en interne par les développeurs I2P.
Nous n'avons aucune preuve que le problème ait jamais été exploité.
La probabilité réelle de succès de l'exploitation peut varier considérablement
selon le protocole et le service au niveau de l'application.
Les applications pair-à-pair sont probablement plus susceptibles d'être affectées
que les applications client/serveur.


## Compatibilité

Aucun problème. Toutes les implémentations connues ignorent actuellement le champ NACKs dans le paquet SYN.
Et même si elles ne l'ignoraient pas, et tentaient de l'interpréter
comme des NACKs pour 8 messages différents, ces messages ne seraient pas en cours 
pendant le processus de SYNCHRONIZE et les NACKs n'auraient aucun sens.


## Migration

Les implémentations peuvent ajouter le support à tout moment, aucune coordination n'est nécessaire.
Les routeurs Java I2P et i2pd ont implémenté cela dans l'API 0.9.58 (publiée en mars 2023).


