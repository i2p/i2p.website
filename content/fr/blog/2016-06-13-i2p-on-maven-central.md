---
title: "I2P sur Maven Central"
date: 2016-06-13
author: "str4d"
description: "Les bibliothèques clientes I2P sont désormais disponibles sur Maven Central !"
categories: ["summer-dev"]
---

Nous sommes presque à mi-parcours du mois des APIs de Summer Dev, et nous faisons de grands progrès sur plusieurs fronts. Je suis heureux d’annoncer que le premier d’entre eux est terminé : les bibliothèques clientes I2P sont désormais disponibles sur Maven Central !

Cela devrait grandement simplifier l’utilisation d’I2P par les développeurs Java dans leurs applications. Au lieu d’avoir à obtenir les bibliothèques depuis une installation existante, ils peuvent simplement ajouter I2P à leurs dépendances. La mise à niveau vers de nouvelles versions sera également beaucoup plus simple.

## Comment les utiliser

Il existe deux bibliothèques que vous devez connaître:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Ajoutez l’un ou les deux à la liste des dépendances de votre projet, et vous êtes opérationnel !

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
Pour d'autres systèmes de build, consultez les pages Maven Central des bibliothèques « core » et « streaming ».

Les développeurs Android devraient utiliser la bibliothèque cliente I2P Android, qui contient les mêmes bibliothèques ainsi que des utilitaires spécifiques à Android. Je vais bientôt la mettre à jour pour qu’elle dépende des nouvelles bibliothèques I2P, afin que les applications multiplateformes puissent fonctionner nativement avec I2P Android ou avec I2P pour ordinateur de bureau.

## Get hacking!

Consultez notre guide de développement d'applications pour vous aider à démarrer avec ces bibliothèques. Vous pouvez aussi discuter avec nous à leur sujet sur #i2p-dev sur IRC. Et si vous commencez à les utiliser, dites-nous sur quoi vous travaillez avec le hashtag #I2PSummer sur Twitter!
