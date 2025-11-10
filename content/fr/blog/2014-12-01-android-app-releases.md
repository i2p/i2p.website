---
title: "Versions de l'application Android"
date: 2014-12-01
author: "str4d"
description: "I2P Android 0.9.17 et Bote 0.3 ont été publiés sur le site web, Google Play et F-Droid."
categories: ["press"]
---

Cela faisait un certain temps que je n'avais pas publié de mises à jour concernant notre développement Android, et plusieurs versions d'I2P sont sorties sans versions Android correspondantes. Enfin, l'attente est terminée !

## Nouvelles versions d’applications

De nouvelles versions d’I2P Android et de Bote ont été publiées ! Elles peuvent être téléchargées à partir de ces URL :

- [I2P Android 0.9.17](https://geti2p.net/en/download#android)
- [Bote 0.3](https://download.i2p.io/android/bote/releases/0.3/Bote.apk)

La principale évolution de ces versions est la transition vers le nouveau système de Material Design d’Android. Material a grandement facilité la création d’applications plus agréables à utiliser pour les développeurs d’applications aux compétences en design, disons, "minimalistes" (comme les miennes). I2P Android met également à jour son I2P router sous-jacent vers la version 0.9.17 tout juste publiée. Bote introduit plusieurs nouvelles fonctionnalités ainsi que de nombreuses petites améliorations ; par exemple, vous pouvez désormais ajouter de nouvelles destinations e-mail via des codes QR.

Comme je l’ai mentionné dans ma dernière mise à jour, la clé de signature utilisée pour signer les applications a changé. La raison, c’est que nous devions changer le nom de package d’I2P Android. L’ancien nom de package (`net.i2p.android.router`) était déjà pris sur Google Play (nous ne savons toujours pas qui l’utilisait), et nous voulions utiliser le même nom de package et la même clé de signature pour toutes les distributions d’I2P Android. Cela signifie qu’un utilisateur peut, dans un premier temps, installer l’application depuis le site web d’I2P, puis, si le site web venait à être bloqué, la mettre à jour via Google Play. Le système d’exploitation Android considère qu’une application est complètement différente lorsque son nom de package change ; nous en avons donc profité pour augmenter la robustesse de la clé de signature.

L'empreinte (SHA-256) de la nouvelle clé de signature est :

```
AD 1E 11 C2 58 46 3E 68 15 A9 86 09 FF 24 A4 8B C0 25 86 C2 36 00 84 9C 16 66 53 97 2F 39 7A 90
```
## Google Play

Il y a quelques mois, nous avons publié I2P Android et Bote sur Google Play en Norvège, afin de tester le processus de publication dans ce pays. Nous sommes heureux d’annoncer que les deux applications sont désormais publiées à l’échelle mondiale par [Privacy Solutions](https://privacysolutions.no/). Les applications sont disponibles aux URL suivantes:

- [I2P on Google Play](https://play.google.com/store/apps/details?id=net.i2p.android)
- [Bote on Google Play](https://play.google.com/store/apps/details?id=i2p.bote.android)

Le déploiement mondial se fait en plusieurs étapes, en commençant par les pays pour lesquels nous disposons de traductions. L’exception notable à cela est la France ; en raison de la réglementation relative à l’importation de code cryptographique, nous ne pouvons pas encore distribuer ces applications sur Google Play France. Il s’agit du même problème qui a touché d’autres applications comme TextSecure et Orbot.

## F-Droid

N’allez pas croire que nous vous avons oubliés, utilisatrices et utilisateurs de F-Droid ! En plus des deux emplacements ci-dessus, nous avons mis en place notre propre dépôt F-Droid. Si vous lisez cet article sur votre téléphone, [cliquez ici](https://f-droid.i2p.io/repo?fingerprint=68E76561AAF3F53DD53BA7C03D795213D0CA1772C3FAC0159B50A5AA85C45DC6) pour l’ajouter à F-Droid (cela ne fonctionne que dans certains navigateurs Android). Ou bien, vous pouvez ajouter manuellement l’URL ci-dessous à votre liste de dépôts F-Droid :

https://f-droid.i2p.io/repo

Si vous souhaitez vérifier manuellement l’empreinte (SHA-256) de la clé de signature du dépôt, ou la saisir lors de l’ajout du dépôt, la voici :

```
68 E7 65 61 AA F3 F5 3D D5 3B A7 C0 3D 79 52 13 D0 CA 17 72 C3 FA C0 15 9B 50 A5 AA 85 C4 5D C6
```
Malheureusement, l'application I2P du dépôt principal F-Droid n'a pas été mise à jour, car notre mainteneur F-Droid est injoignable. Nous espérons qu'en maintenant ce dépôt binaire, nous pourrons mieux prendre en charge nos utilisateurs F-Droid et les maintenir à jour. Si vous avez déjà installé I2P depuis le dépôt principal F-Droid, vous devrez désinstaller l'application si vous souhaitez effectuer la mise à jour, car la clé de signature sera différente. Les applications de notre dépôt F-Droid sont identiques aux APK proposées sur notre site web et sur Google Play, ainsi, à l'avenir vous pourrez mettre à jour en utilisant n'importe laquelle de ces sources.
