---
title: "Types MIME I2P"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Vue d'ensemble

Définir les types MIME pour les formats de fichiers courants d'I2P.
Inclure les définitions dans les paquets Debian.
Fournir un gestionnaire pour le type .su3, et possiblement d'autres.


## Motivation

Pour faciliter le réensemencement et l'installation de plugins lors du téléchargement avec un navigateur,
nous avons besoin d'un type MIME et d'un gestionnaire pour les fichiers .su3.

Tant que nous y sommes, après avoir appris à écrire le fichier de définition MIME,
suivant la norme freedesktop.org, nous pouvons ajouter des définitions pour d'autres
types de fichiers I2P courants.
Bien que moins utile pour les fichiers qui ne sont pas habituellement téléchargés, tels que
la base de données adressebook blockfile (hostsdb.blockfile), ces définitions permettent
une meilleure identification et iconification des fichiers lorsqu'on utilise un visualiseur
de répertoires graphiques tel que "nautilus" sur Ubuntu.

En standardisant les types MIME, chaque implémentation de routeur peut écrire des gestionnaires
appropriés, et le fichier de définition MIME peut être partagé par toutes les implémentations.


## Conception

Écrire un fichier source XML suivant la norme freedesktop.org et l'inclure
dans les paquets Debian. Le fichier est "debian/(package).sharedmimeinfo".

Tous les types MIME d'I2P commenceront par "application/x-i2p-", sauf pour le jrobin rrd.

Les gestionnaires pour ces types MIME sont spécifiques à l'application et ne seront pas
spécifiés ici.

Nous inclurons également les définitions avec Jetty, et les inclurons avec
le logiciel de réensemencement ou des instructions.


## Spécifications

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(générique)	application/x-i2p-su3

.su3	(mise à jour du routeur)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(réensemencement)	application/x-i2p-su3-reseed

.su3	(nouvelles)		application/x-i2p-su3-news

.su3	(liste de blocage)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Remarques

Tous les formats de fichiers listés ci-dessus ne sont pas utilisés par les implémentations de routeur non-Java;
certains peuvent même ne pas être bien définis. Cependant, les documenter ici
peut permettre une cohérence entre implémentations à l'avenir.

Certaines extensions de fichier telles que ".config", ".dat" et ".info" peuvent chevaucher d'autres
types MIME. Elles peuvent être désambiguës avec des données supplémentaires telles que
le nom de fichier complet, un motif de nom de fichier, ou des nombres magiques.
Voir le fichier brouillon i2p.sharedmimeinfo dans le fil zzz.i2p pour des exemples.

Les types importants sont les types .su3, et ces types ont à la fois
une extension unique et des définitions de nombres magiques robustes.


## Migration

Non applicable.
