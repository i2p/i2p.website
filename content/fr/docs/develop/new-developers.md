---
title: "Guide du Nouveau Développeur"
description: "Comment commencer à contribuer à I2P : matériel d'étude, code source, compilation, idées, publication, communauté, traductions et outils"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: mettre à jour la partie traduction
---

Vous souhaitez donc commencer à travailler sur I2P ? Excellent ! Voici un guide rapide pour débuter et contribuer au site web ou au logiciel, effectuer du développement ou créer des traductions.

Pas encore prêt à coder ? Essayez d'abord de [vous impliquer](/get-involved/).

## Apprendre à connaître Java

Le router I2P et ses applications intégrées utilisent Java comme langage de développement principal. Si vous n'avez pas d'expérience avec Java, vous pouvez toujours consulter [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)

Étudiez l'introduction pratique, les autres documents « comment faire », l'introduction technique et les documents associés :

- Comment introduction : [Introduction à I2P](/docs/overview/intro/)
- Hub de documentation : [Documentation](/docs/)
- Introduction technique : [Introduction technique](/docs/overview/tech-intro/)

Cela vous donnera un bon aperçu de la structure d'I2P et des différentes fonctions qu'il accomplit.

## Obtenir le code I2P

Pour le développement sur le routeur I2P ou les applications intégrées, vous devez obtenir le code source.

### Notre méthode actuelle : Git

I2P dispose de services Git officiels et accepte les contributions via Git sur notre propre GitLab :

- À l'intérieur d'I2P : <http://git.idk.i2p>
- À l'extérieur d'I2P : <https://i2pgit.org>

Clonez le dépôt principal :

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
Un miroir en lecture seule est également disponible sur GitHub :

- Miroir GitHub : [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## Compilation d'I2P

Pour compiler le code, vous avez besoin du Sun/Oracle Java Development Kit 6 ou supérieur, ou d'un JDK équivalent (Sun/Oracle JDK 6 fortement recommandé) et d'Apache Ant version 1.7.0 ou supérieure. Si vous travaillez sur le code principal d'I2P, allez dans le répertoire `i2p.i2p` et exécutez `ant` pour voir les options de compilation.

Pour compiler ou travailler sur les traductions de la console, vous avez besoin des outils `xgettext`, `msgfmt` et `msgmerge` du paquet GNU gettext.

Pour le développement de nouvelles applications, consultez le [guide de développement d'applications](/docs/develop/applications/).

## Idées de développement

Consultez la liste TODO du projet ou la liste des problèmes sur GitLab pour des idées :

- Tickets GitLab : [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Rendre les résultats disponibles

Consultez le bas de la page des licences pour connaître les exigences relatives aux privilèges de commit. Vous en avez besoin pour intégrer du code dans `i2p.i2p` (non requis pour le site web !).

- [Page des licences](/docs/develop/licenses#commit)

## Faites notre connaissance !

Les développeurs traînent sur IRC. Ils peuvent être contactés sur différents réseaux et sur les réseaux internes I2P. L'endroit habituel pour les trouver est `#i2p-dev`. Rejoignez le canal et dites bonjour ! Nous avons également des [directives supplémentaires pour les développeurs réguliers](/docs/develop/dev-guidelines/).

## Traductions

Traducteurs du site web et de la console du routeur : Consultez le [Guide du nouveau traducteur](/docs/develop/new-translators/) pour les prochaines étapes.

## Outils

I2P est un logiciel open source principalement développé à l'aide d'outils open source. Le projet I2P a récemment obtenu une licence pour YourKit Java Profiler. Les projets open source peuvent bénéficier d'une licence gratuite à condition que YourKit soit mentionné sur le site web du projet. N'hésitez pas à nous contacter si vous souhaitez profiler la base de code I2P.

YourKit soutient généreusement les projets open source avec ses profileurs complets. YourKit, LLC est le créateur d'outils innovants et intelligents pour le profilage d'applications Java et .NET. Découvrez les logiciels de pointe de YourKit :

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
