---
title: "Notes de statut d’I2P du 2004-08-24"
date: 2004-08-24
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P couvrant la version 0.3.4.3, de nouvelles fonctionnalités de la console du router, l’avancement de la 0.4 et diverses améliorations"
categories: ["status"]
---

Bonjour à tous, beaucoup de mises à jour aujourd'hui

## Index

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 statut

La version 0.3.4.3 est sortie vendredi dernier et, depuis, les choses se passent plutôt bien. Il y a eu quelques problèmes avec du code nouvellement introduit pour les tests de tunnel et la sélection des pairs, mais après quelques ajustements depuis la publication, c’est désormais assez solide. Je ne sais pas si le serveur IRC est déjà sur la nouvelle révision, donc nous devons généralement nous appuyer sur des tests avec des eepsites(sites I2P) et les outproxies HTTP (mandataires sortants HTTP) (squid.i2p et www1.squid.i2p). Les transferts de fichiers volumineux (>5 Mo) dans la version 0.3.4.3 ne sont toujours pas suffisamment fiables, mais d’après mes tests, les modifications depuis lors ont encore amélioré les choses.

Le réseau a également grandi - nous avons atteint 45 utilisateurs simultanés plus tôt aujourd’hui, et nous nous situons régulièrement dans la fourchette de 38 à 44 utilisateurs depuis quelques jours (w00t) ! C’est un niveau sain pour le moment, et je surveille l’activité globale du réseau pour repérer d’éventuels risques. Lors du passage à la version 0.4, nous voudrons augmenter progressivement la base d’utilisateurs jusqu’à atteindre environ le cap des 100 router et effectuer encore quelques tests avant d’aller plus loin. Du moins, c’est mon objectif du point de vue d’un développeur.

### 1.1) timestamper

L’une des nouveautés vraiment géniales introduites avec la version 0.3.4.3, que j’ai complètement oublié de mentionner, est une mise à jour du code SNTP. Grâce à la générosité d’Adam Buckley, qui a accepté de publier son code SNTP sous licence BSD, nous avons fusionné l’ancienne application Timestamper au cœur de l’I2P SDK et l’avons entièrement intégrée à notre horloge. Cela signifie trois choses : 1. vous pouvez supprimer le timestamper.jar (le code est désormais dans i2p.jar) 2. vous pouvez retirer les lignes clientApp associées de votre configuration 3. vous pouvez mettre à jour votre configuration pour utiliser les nouvelles options de synchronisation de l’heure

Les nouvelles options dans le fichier router.config sont simples, et les valeurs par défaut devraient suffire (d'autant plus que la majorité d'entre vous les utilise sans s'en rendre compte :)

Pour définir la liste des serveurs SNTP à interroger:

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
Pour désactiver la synchronisation de l'heure (uniquement si vous êtes un gourou NTP et savez que l'horloge de votre système d'exploitation est *toujours* exacte - exécuter "windows time" n'est PAS suffisant) :

```
time.disabled=true
```
Vous n'avez plus besoin d'avoir un 'timestamper password' (mot de passe d'horodatage), puisque tout est directement intégré dans le code (ah, les joies de BSD vs GPL :)

### 1.2) new router console authentication

Ceci ne concerne que celles et ceux d’entre vous qui exécutent la nouvelle console du router, mais si elle écoute sur une interface publique, vous voudrez peut‑être tirer parti de l’authentification HTTP basique intégrée. Oui, l’authentification HTTP basique est ridiculement faible — elle ne vous protégera pas contre quelqu’un qui sniffe votre réseau ou tente une attaque par force brute, mais elle tiendra à l’écart les curieux occasionnels. Quoi qu’il en soit, pour l’utiliser, ajoutez simplement la ligne

```
consolePassword=blah
```
dans votre router.config. Vous devrez malheureusement redémarrer le router, car ce paramètre n'est transmis à Jetty qu'une seule fois (au démarrage).

## 2) 0.4 status

Nous faisons beaucoup de progrès sur la version 0.4, et nous espérons publier des préversions au cours de la semaine prochaine. Nous sommes toutefois encore en train de peaufiner certains détails, donc nous n’avons pas encore mis en place un processus de mise à niveau solide. La version sera rétrocompatible, donc la mise à jour ne devrait pas être trop pénible. Quoi qu’il en soit, restez à l’écoute et vous saurez quand tout sera prêt.

### 1.1) horodateur

Hypercubus réalise de grands progrès dans l’intégration du programme d’installation, d’une application systray (zone de notification système) et d’un code de gestion des services. En bref, pour la version 0.4, tous les utilisateurs Windows auront automatiquement une petite icône systray (Iggy!), bien qu’ils puissent la désactiver (et/ou la réactiver) via la console web. De plus, nous allons inclure le JavaService wrapper, qui nous permettra de faire toutes sortes de choses pratiques, comme lancer I2P au démarrage du système (ou non), redémarrer automatiquement dans certaines conditions, effectuer un redémarrage forcé de la JVM à la demande, générer des traces de pile, et bien d’autres fonctionnalités.

### 1.2) nouvelle authentification de la console du router

L’une des grandes nouveautés de la version 0.4 sera une refonte du code jbigi, en y intégrant les modifications qu’Iakin a apportées pour Freenet ainsi que la nouvelle bibliothèque native "jcpuid" d’Iakin. La bibliothèque jcpuid ne fonctionne que sur des architectures x86 et, de concert avec du nouveau code jbigi, déterminera la version jbigi 'appropriée' à charger. En conséquence, nous livrerons un unique jbigi.jar que tout le monde aura, et à partir de celui-ci nous sélectionnerons la version 'appropriée' pour la machine actuelle. Les utilisateurs pourront bien sûr toujours compiler leur propre jbigi natif, en écrasant la sélection de jcpuid (il suffit de le compiler et de le copier dans votre répertoire d’installation I2P, ou de le nommer "jbigi" et de le placer dans un fichier .jar présent dans votre classpath (chemin de classes Java)). Cependant, en raison des mises à jour, ce n’est *pas* rétrocompatible - lors de la mise à niveau, vous devez soit recompiler votre propre jbigi, soit supprimer votre bibliothèque native existante (pour laisser le nouveau code jcpuid choisir la bonne version).

### 2.3) i2paddresshelper

oOo a mis au point un outil très pratique permettant aux utilisateurs de naviguer sur des eepsites(I2P Sites) sans mettre à jour leur hosts.txt. Il a été intégré à CVS et sera déployé dans la prochaine version, mais il peut être pertinent d’envisager de mettre à jour les liens en conséquence (cervantes a mis à jour le [i2p] bbcode de forum.i2p pour le prendre en charge avec un lien « Try it [i2p] »).

En pratique, il suffit de créer un lien vers l’eepsite(site I2P) avec le nom de votre choix, puis d’y ajouter un paramètre d’URL spécial précisant la destination :

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
Sous le capot, c’est assez sûr — vous ne pouvez pas usurper une autre adresse, et le nom n’est *pas* enregistré dans hosts.txt, mais cela vous permettra de voir les images, etc., référencées sur des eepsites(I2P Sites) que vous ne pourriez pas voir avec l’ancienne astuce `http://i2p/base64/`. Si vous voulez toujours pouvoir utiliser "wowthisiscool.i2p" pour accéder à ce site, il vous faudra bien sûr encore ajouter l’entrée à votre hosts.txt (jusqu’à ce que le carnet d’adresses MyI2P soit déployé, bien sûr ;)

## 3) AMOC vs. restricted routes

Mule a rassemblé quelques idées et m’a poussé à expliquer certaines choses, et, ce faisant, il a réussi à me faire réévaluer toute l’idée AMOC. Plus précisément, si nous abandonnons l’une des contraintes que j’ai imposées à notre couche de transport - ce qui nous permettrait de supposer la bidirectionnalité - nous pourrions abandonner complètement le transport AMOC pour plutôt mettre en œuvre quelques mécanismes élémentaires de routage restreint (en posant les bases de techniques de routage restreint plus avancées, comme des pairs de confiance et des router tunnels multi-sauts, pour plus tard).

Si nous choisissons cette approche, cela voudrait dire que les personnes pourraient participer au réseau derrière des pare-feu, des NAT (traduction d’adresses réseau), etc., sans aucune configuration, et offrirait également certaines des propriétés d’anonymat des routes restreintes. En retour, cela entraînerait probablement une refonte importante de notre feuille de route, mais si nous pouvons le faire en toute sécurité, cela nous ferait gagner un temps fou et vaudrait largement le changement.

Cependant, nous ne voulons pas nous précipiter et nous devrons examiner attentivement les implications en matière d'anonymat et de sécurité avant de nous engager dans cette voie. Nous le ferons après la sortie de la version 0.4 et une fois que tout se déroulera sans accroc, il n'y a donc pas d'urgence.

## 2) 0.4 statut

D’après les bruits qui courent, aum fait de bons progrès - je ne sais pas s’il sera présent à la réunion pour nous donner une mise à jour, mais il nous a laissé un petit message sur #i2p ce matin :

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
Youpi.

## 5) pages of note

Je souhaite simplement signaler deux nouvelles ressources disponibles que les utilisateurs d’I2P voudront peut-être consulter : DrWoo a mis en place une page rassemblant de nombreuses informations pour les personnes qui souhaitent naviguer anonymement, et Luckypunk a publié un guide (howto) décrivant ses expériences avec certaines JVM sous FreeBSD. Hypercubus a également publié la documentation sur les tests de l’intégration, pas encore publiée, du service et du systray (zone de notification).

## 6) ???

Ok, c'est tout ce que j'ai à dire pour le moment - venez à la réunion ce soir à 21 h GMT si vous voulez aborder autre chose.

=jr
