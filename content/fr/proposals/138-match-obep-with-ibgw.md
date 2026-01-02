---
title: "Associer les OBEP avec les IBGW"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Open"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Aperçu

Cette proposition ajoute une option I2CP pour les tunnels sortants qui permet de
choisir ou de construire des tunnels lorsqu'un message est envoyé de sorte que l'OBEP corresponde à l'un des IBGW du LeaseSet pour la Destination cible.


## Motivation

La plupart des routeurs I2P utilisent une forme de suppression de paquets pour la gestion de la congestion. L'implémentation de référence utilise une stratégie WRED qui prend en compte à la fois la taille du message et la distance parcourue (voir [documentation tunnel throttling](/docs/specs/implementation/#tunnelthrottling)). En raison de cette stratégie, la principale source de perte de paquets est l'OBEP.


## Conception

Lors de l'envoi d'un message, l'expéditeur choisit ou construit un tunnel avec un OBEP qui est le même routeur que l'un des IBGW du destinataire. Ainsi, le message sortira directement d'un tunnel et entrera dans l'autre, sans avoir besoin d'être envoyé via le réseau entre les deux.


## Implications de sécurité

Ce mode signifierait effectivement que le destinataire sélectionne l'OBEP de l'expéditeur. Pour maintenir la confidentialité actuelle, ce mode entraînerait la construction de tunnels sortants d'un saut plus long que celui spécifié par l'option outbound.length de l'I2CP (le dernier saut pouvant éventuellement être en dehors du niveau rapide de l'expéditeur).


## Spécification

Une nouvelle option I2CP est ajoutée à la [spécification I2CP](/docs/specs/i2cp/) :

    outbound.matchEndWithTarget
        Booléen

        Valeur par défaut : spécifique au cas

        Si true, le routeur choisira des tunnels sortants pour les messages envoyés
        pendant cette session de manière que l'OBEP du tunnel soit l'un des IBGW pour la
        Destination cible. Si un tel tunnel n'existe pas, le routeur en construira un.


## Compatibilité

La rétrocompatibilité est assurée, puisque les routeurs peuvent toujours s'envoyer des messages à eux-mêmes.


## Implémentation

### Java I2P

La construction de tunnels et l'envoi de messages sont actuellement des sous-systèmes séparés :

- BuildExecutor ne connaît que les options outbound.* du pool de tunnels sortants,
  et n'a pas de visibilité concernant leur utilisation.

- OutboundClientMessageOneShotJob ne peut que sélectionner un tunnel dans le pool existant ; si un message client arrive et qu'il n'y a pas de tunnels sortants, le routeur supprime le message.

Implémenter cette proposition nécessiterait de concevoir un moyen pour que ces deux
sous-systèmes interagissent.

### i2pd

Une implémentation de test a été complétée.


## Performance

Cette proposition a divers effets sur la latence, le RTT et la perte de paquets :

- Il est probable que dans la plupart des cas, ce mode nécessiterait la construction d'un nouveau tunnel
  dès le premier message plutôt que d'utiliser un tunnel existant, ajoutant ainsi de la latence.

- Pour les tunnels standards, l'OBEP pourrait avoir besoin de trouver et de se connecter à l'IBGW,
  ajoutant une latence qui augmente le premier RTT (car cela se produit après l'envoi du premier
  paquet). En utilisant ce mode, l'OBEP devrait trouver et se connecter à l'IBGW lors de la construction
  du tunnel, ajoutant la même latence mais réduisant le premier RTT (car cela se produit avant
  l'envoi du premier paquet).

- La taille VariableTunnelBuild actuellement standard est de 2641 octets. Il est donc attendu que
  ce mode entraîne une moindre perte de paquets pour les tailles de message moyennes supérieures à cela.

Davantage de recherche est nécessaire pour étudier ces effets, afin de décider
quels tunnels standards bénéficieraient de ce mode activé par défaut.
