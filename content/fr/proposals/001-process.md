---
title: "Le Processus de Proposition I2P"
number: "001"
author: "str4d"
created: "2016-04-10"
lastupdated: "2017-04-07"
status: "Meta"
thread: "http://zzz.i2p/topics/1980"
---

## Aperçu

Ce document décrit comment modifier les spécifications I2P, comment fonctionnent les propositions I2P, et la relation entre les propositions I2P et les spécifications.

Ce document est adapté du processus de proposition Tor, et la plupart du contenu ci-dessous a été initialement rédigé par Nick Mathewson.

Ceci est un document informatif.

## Motivation

Auparavant, notre processus pour mettre à jour les spécifications I2P était relativement informel : nous faisions une proposition sur le forum de développement et discutions des modifications, puis nous atteignions un consensus et modifions la spécification avec des modifications de brouillon (pas nécessairement dans cet ordre), et finalement nous implémentions les modifications.

Cela posait quelques problèmes.

Premièrement, même dans son état le plus efficace, l'ancien processus laissait souvent la spécification désynchronisée avec le code. Les pires cas étaient ceux où l'implémentation était différée : la spécification et le code pouvaient rester désynchronisés pendant plusieurs versions.

Deuxièmement, il était difficile de participer à la discussion, car il n'était pas toujours clair quelles parties de la discussion étaient incluses dans la proposition, ou quelles modifications de la spécification avaient été implémentées. Les forums de développement ne sont accessibles qu'à l'intérieur d'I2P, ce qui signifie que les propositions ne pouvaient être vues que par les personnes utilisant I2P.

Troisièmement, il était très facile d'oublier certaines propositions car elles pouvaient se retrouver enfouies plusieurs pages en arrière dans la liste des discussions du forum.

## Comment changer les spécifications maintenant

Premièrement, quelqu'un rédige un document de proposition. Il doit décrire en détail le changement à réaliser, et donner une idée de comment l'implémenter. Une fois suffisamment étoffé, cela devient une proposition.

Comme un RFC, chaque proposition reçoit un numéro. Contrairement aux RFC, les propositions peuvent évoluer au fil du temps et garder le même numéro, jusqu'à ce qu'elles soient finalement acceptées ou rejetées. L'historique de chaque proposition sera stocké dans le dépôt du site web I2P.

Une fois une proposition dans le dépôt, nous devrions en discuter sur le fil correspondant et l'améliorer jusqu'à ce que nous soyons parvenus à un consensus que c'est une bonne idée, et qu'elle est suffisamment détaillée pour être implémentée. Lorsque cela se produit, nous implémentons la proposition et l'intégrons dans les spécifications. Ainsi, les spécifications demeurent la documentation canonique pour le protocole I2P : aucune proposition n'est jamais la documentation canonique pour une fonctionnalité implémentée.

(Ce processus ressemble assez au processus d'amélioration de Python, à ceci près que les propositions I2P sont réintégrées dans les spécifications après implémentation, tandis que les PEP *deviennent* la nouvelle spécification.)

### Changements mineurs

Il est toujours possible de faire de petits changements directement dans la spécification si le code peut être rédigé à peu près immédiatement, ou des changements cosmétiques si aucun changement de code n'est requis. Ce document reflète l'*intention* actuelle des développeurs, pas une promesse permanente d'utiliser toujours ce processus à l'avenir : nous nous réservons le droit de vraiment nous enthousiasmer et de courir implémenter quelque chose lors d'une session de hacking toute la nuit stimulée par le café ou les M&M.

## Comment de nouvelles propositions sont ajoutées

Pour soumettre une proposition, postez-la sur le forum de développement ou entrez un ticket avec la proposition attachée.

Une fois qu'une idée a été proposée, qu'un brouillon correctement formaté (voir ci-dessous) existe, et qu'un consensus approximatif au sein de la communauté active de développement existe pour dire que cette idée mérite d'être examinée, les éditeurs de propositions ajouteront officiellement la proposition.

Les éditeurs de propositions actuels sont zzz et str4d.

## Ce qui doit figurer dans une proposition

Chaque proposition doit avoir un en-tête contenant les champs suivants :

```
:author:
:created:
:thread:
:lastupdated:
:status:
```

- Le champ `author` doit contenir les noms des auteurs de cette proposition.
- Le champ `thread` doit être un lien vers le fil du forum de développement où cette proposition a été initialement postée, ou vers un nouveau fil créé pour discuter de cette proposition.
- Le champ `lastupdated` doit initialement être égal au champ `created`, et doit être mis à jour chaque fois que la proposition est modifiée.

Ces champs doivent être définis selon les besoins :

```
:supercedes:
:supercededby:
:editor:
```

- Le champ `supercedes` est une liste, séparée par des virgules, de toutes les propositions que cette proposition remplace. Ces propositions devraient être Rejetées et avoir leur champ `supercededby` mis au numéro de cette proposition.
- Le champ `editor` doit être défini si des changements significatifs sont effectués à cette proposition sans en altérer substantiellement le contenu. Si le contenu est substantiellement modifié, un `author` supplémentaire doit être ajouté, ou une nouvelle proposition créée remplaçant celle-ci.

Ces champs sont optionnels mais recommandés :

```
:target:
:implementedin:
```

- Le champ `target` doit décrire pour quelle version la proposition est censée être implémentée (si elle est Ouverte ou Acceptée).
- Le champ `implementedin` doit décrire dans quelle version la proposition a été implémentée (si elle est Terminée ou Fermée).

Le corps de la proposition doit commencer par une section Aperçu expliquant de quoi parle la proposition, ce qu'elle fait, et dans quel état elle se trouve.

Après l'Aperçu, la proposition devient plus librement formatée. En fonction de sa longueur et de sa complexité, la proposition peut se diviser en sections de manière appropriée, ou suivre un format discursif court. Chaque proposition doit contenir au moins les informations suivantes avant d'être Acceptée, bien qu'elles ne doivent pas nécessairement être dans des sections portant ces noms.

**Motivation**
: Quel problème la proposition essaie-t-elle de résoudre ? Pourquoi ce problème importe-t-il ? Si plusieurs approches sont possibles, pourquoi choisir celle-ci ?

**Conception**
: Une vue d'ensemble des fonctionnalités nouvelles ou modifiées, comment elles fonctionnent, comment elles interagissent entre elles, et comment elles interagissent avec le reste d'I2P. C'est le corps principal de la proposition. Certaines propositions commenceront uniquement avec une Motivation et une Conception et attendront une spécification jusqu'à ce que la Conception semble appropriée.

**Implications en matière de sécurité**
: Quels effets les changements proposés pourraient avoir sur l'anonymat, à quel point ces effets sont bien compris, etc.

**Spécification**
: Une description détaillée de ce qui doit être ajouté aux spécifications I2P pour implémenter la proposition. Elle doit être suffisamment détaillée pour permettre à des programmeurs indépendants d'écrire des implémentations compatibles entre elles de la proposition basées sur ses spécifications.

**Compatibilité**
: Les versions d'I2P suivant la proposition seront-elles compatibles avec les versions qui ne la suivent pas ? Si oui, comment la compatibilité sera-t-elle assurée ? Nous essayons généralement de ne pas abandonner la compatibilité si possible ; nous n'avons pas effectué de changement "journée drapeau" depuis mars 2008 et nous ne voulons pas en faire un autre.

**Implémentation**
: Si la proposition est difficile à implémenter dans l'architecture actuelle d'I2P, le document peut contenir une discussion sur la façon de procéder pour la faire fonctionner. Les vrais correctifs devraient être sur des branches publiques monotone, ou téléchargés sur Trac.

**Notes sur la performance et la scalabilité**
: Si la fonctionnalité a un effet sur la performance (en RAM, CPU, bande passante) ou sur la scalabilité, il devrait y avoir une analyse de l'importance de cet effet, afin d'éviter des régressions de performance coûteuses, et pour éviter de perdre du temps sur des gains insignifiants.

**Références**
: Si la proposition se réfère à des documents externes, ceux-ci devraient être listés.

## Statut de la proposition

**Ouverte**
: Une proposition en discussion.

**Acceptée**
: La proposition est complète, et nous avons l'intention de l'implémenter. Après ce point, il faut éviter les changements substantiels à la proposition, et les considérer comme un signe d'échec du processus quelque part.

**Terminée**
: La proposition a été acceptée et implémentée. Après ce point, la proposition ne devrait pas être modifiée.

**Fermée**
: La proposition a été acceptée, implémentée, et intégrée dans les documents de spécification principaux. La proposition ne devrait plus être changée après ce point.

**Rejetée**
: Nous n'allons pas implémenter la fonctionnalité telle que décrite ici, bien que nous puissions envisager une autre version. Voir les commentaires dans le document pour plus de détails. La proposition ne doit pas être changée après ce point ; pour proposer une autre version de l'idée, rédigez une nouvelle proposition.

**Brouillon**
: Ceci n'est pas encore une proposition complète ; il manque des éléments évidents. Veuillez ne pas ajouter de nouvelles propositions avec ce statut ; mettez-les plutôt dans le sous-répertoire "idées".

**Nécessite des révisions**
: L'idée de la proposition est bonne, mais la proposition telle qu'elle est a des problèmes graves qui empêchent son acceptation. Voir les commentaires dans le document pour plus de détails.

**Morte**
: La proposition n'a pas été touchée depuis longtemps, et il ne semble pas que quelqu'un la complètera bientôt. Elle peut redevenir "Ouverte" si elle obtient un nouveau partisan.

**Nécessite des recherches**
: Il y a des problèmes de recherche qui doivent être résolus avant qu'il ne soit clair si la proposition est une bonne idée.

**Meta**
: Ce n'est pas une proposition, mais un document sur les propositions.

**Réserve**
: Cette proposition n'est pas quelque chose que nous prévoyons actuellement d'implémenter, mais nous pourrions vouloir la ressusciter un jour si nous décidons de faire quelque chose de similaire à ce qu'elle propose.

**Informationnel**
: Cette proposition est la dernière information sur ce qu'elle fait. Elle ne deviendra pas une spécification à moins que quelqu'un ne la copie et ne l'intègre dans une nouvelle spécification pour un nouveau sous-système.

Les éditeurs maintiennent le statut correct des propositions, basé sur un consensus approximatif et leur propre discrétion.

## Numérotation des propositions

Les numéros 000-099 sont réservés aux propositions spéciales et méta-propositions. Les numéros 100 et suivants sont utilisés pour les propositions réelles. Les numéros ne sont pas réutilisés.

## Références

- [Processus de Proposition Tor](https://gitweb.torproject.org/torspec.git/tree/proposals/001-process.txt)
