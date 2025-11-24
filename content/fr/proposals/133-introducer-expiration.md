---
title: "Expiration de l'Introcuteur"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Closed"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Aperçu

Cette proposition concerne l'amélioration du taux de succès pour les introductions.


## Motivation

Les introducteurs expirent après un certain temps, mais cette information n'est pas publiée dans le
RouterInfo. Les routeurs doivent actuellement utiliser des heuristiques pour estimer quand un
introducteur n'est plus valide.


## Conception

Dans une RouterAddress SSU contenant des introducteurs, l'éditeur peut éventuellement
inclure des temps d'expiration pour chaque introducteur.


## Spécification

```
iexp{X}={nnnnnnnnnn}

X :: Le numéro de l'introducteur (0-2)

nnnnnnnnnn :: Le temps en secondes (pas ms) depuis l'époque.
```

### Notes
* Chaque expiration doit être supérieure à la date de publication du RouterInfo,
  et inférieure à 6 heures après la date de publication du RouterInfo.

* Les routeurs et introducteurs publieurs doivent tenter de maintenir l'introducteur valide
  jusqu'à l'expiration, cependant il n'y a aucun moyen pour eux de garantir cela.

* Les routeurs ne doivent pas utiliser un introducteur publié après son expiration.

* Les expirations d'introducteur sont dans le mappage RouterAddress.
  Elles ne sont pas le champ d'expiration de 8 octets (actuellement inutilisé) dans le RouterAddress.

**Exemple :** `iexp0=1486309470`


## Migration

Aucun problème. L'implémentation est facultative.
La compatibilité ascendante est assurée, car les anciens routeurs ignoreront les paramètres inconnus.
