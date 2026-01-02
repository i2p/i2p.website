---
title: "Pays stricts/restrictifs"
description: "Comment I2P se comporte dans les juridictions où le routage ou les outils d'anonymat sont restreints (Mode Caché et liste stricte)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

Cette implémentation d'I2P (l'implémentation Java distribuée sur ce site) inclut une « Liste des pays stricts » utilisée pour ajuster le comportement du router dans les régions où participer au routage pour d'autres utilisateurs peut être restreint par la loi. Bien que nous n'ayons pas connaissance de juridictions interdisant l'utilisation d'I2P, plusieurs ont des interdictions générales concernant le relais de trafic. Les routers qui semblent se trouver dans des pays « stricts » sont automatiquement placés en mode Caché.

Le Projet fait référence aux recherches d'organisations de droits civils et numériques lors de la prise de ces décisions. En particulier, les recherches continues de Freedom House guident nos choix. La recommandation générale est d'inclure les pays avec un score de Libertés Civiles (CL) de 16 ou moins, ou un score de Liberté Internet de 39 ou moins (non libre).

## Résumé du mode caché

Lorsqu'un routeur est placé en mode Caché, trois éléments clés changent dans son comportement :

- Il ne publie pas de RouterInfo dans la netDb.
- Il n'accepte pas les tunnels participants.
- Il rejette les connexions directes aux routeurs situés dans le même pays.

Ces défenses rendent les routeurs plus difficiles à énumérer de manière fiable et réduisent le risque de violer les interdictions locales concernant le relais du trafic pour autrui.

## Liste des pays stricts (en 2024)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
Si vous pensez qu'un pays devrait être ajouté ou retiré de la liste stricte, veuillez ouvrir un ticket : https://i2pgit.org/i2p/i2p.i2p/

Référence : Freedom House – https://freedomhouse.org/
