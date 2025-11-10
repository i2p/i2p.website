---
title: "Comment basculer vers le service Outproxy StormyCloud"
date: 2022-08-04
author: "idk"
description: "Comment passer au service Outproxy StormyCloud"
categories: ["general"]
API_Translate: vrai
---

## Comment basculer vers le service de proxy sortant StormyCloud

**Un nouveau proxy de sortie professionnel**

Depuis des années, I2P n’a eu qu’un seul outproxy (proxy de sortie) par défaut, `false.i2p`, dont la fiabilité s’est dégradée. Bien que plusieurs concurrents soient apparus pour prendre une partie du relais, ils ne sont pour la plupart pas en mesure de se porter volontaires pour prendre en charge, par défaut, les clients d’une implémentation I2P entière. Cependant, StormyCloud, une organisation professionnelle à but non lucratif qui exploite des nœuds de sortie Tor, a lancé un nouveau service d’outproxy professionnel, testé par des membres de la communauté I2P, qui deviendra le nouvel outproxy par défaut dans la prochaine version.

**Qui sont StormyCloud**

Selon leurs propres termes, StormyCloud est :

> Mission de StormyCloud Inc : défendre l'accès à Internet comme un droit humain universel. Ce faisant, le groupe protège la vie privée électronique des utilisateurs et renforce la communauté en favorisant un accès sans restriction à l'information et donc le libre échange d'idées au-delà des frontières. C'est essentiel, car Internet est l'outil le plus puissant dont nous disposons pour avoir un impact positif dans le monde.

> Matériel : Nous possédons l’ensemble de notre matériel et nous hébergeons actuellement nos équipements en colocation dans un centre de données Tier 4. À l’heure actuelle, nous disposons d’une liaison montante de 10GBps, avec la possibilité de passer à 40GBps sans nécessiter de grands changements. Nous avons notre propre ASN (numéro de système autonome) et notre propre espace d’adresses IP (IPv4 et IPv6).

Pour en savoir plus sur StormyCloud, visitez leur [site web](https://www.stormycloud.org/).

Sinon, visitez-les sur [I2P](http://stormycloud.i2p/).

**Passage au proxy de sortie StormyCloud sur I2P**

Pour passer à l’outproxy (mandataire de sortie) StormyCloud *aujourd’hui*, vous pouvez vous rendre sur [le Gestionnaire des services cachés](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0). Une fois sur cette page, remplacez la valeur de **Outproxies** et **SSL Outproxies** par `exit.stormycloud.i2p`. Une fois cela fait, faites défiler jusqu’en bas de la page et cliquez sur le bouton "Save".

**Merci à StormyCloud**

Nous remercions StormyCloud de s’être porté volontaire pour fournir au réseau I2P des services d’outproxy (proxy de sortie) de haute qualité.
