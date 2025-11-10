---
title: "Récupération d'information BEP9"
number: "107"
author: "sponge"
created: "2011-02-23"
lastupdated: "2011-02-23"
status: "Mort"
thread: "http://zzz.i2p/topics/860"
---

## Vue d'ensemble

Cette proposition concerne l'ajout d'une récupération complète d'information à l'implémentation I2P du BEP9.


## Motivation

BEP9 ne transmet pas le fichier torrent entier, entraînant ainsi la perte de plusieurs éléments importants du dictionnaire et modifiant le SHA1 total des fichiers torrent. Cela est problématique pour les liens maggot et également parce que des informations importantes sont perdues. Les listes de trackers, les commentaires et toutes données supplémentaires disparaissent. Un moyen de récupérer ces informations est crucial, et cela doit ajouter le moins possible au fichier torrent. Il ne doit pas non plus y avoir de dépendance circulaire. Les informations de récupération ne doivent en aucun cas affecter les clients actuels. Les torrents sans tracker (l'URL du tracker est littéralement 'sans tracker') ne contiennent pas le champ supplémentaire, car ils sont spécifiques à l'utilisation du protocole maggot pour la découverte et le téléchargement, ce qui ne perd jamais les informations en premier lieu.


## Solution

Tout ce qui est nécessaire est de compresser les informations qui seraient perdues et de les stocker dans le dictionnaire info.


### Implémentation
1. Générer le dictionnaire info habituel.
2. Générer le dictionnaire principal et omettre l'entrée info.
3. Encodage B, puis compression du dictionnaire principal avec gzip.
4. Ajouter le dictionnaire principal compressé au dictionnaire info.
5. Ajouter les infos dans le dictionnaire principal.
6. Écrire le fichier torrent.

### Récupération
1. Décompresser l'entrée de récupération dans le dict info.
2. Décoder l'entrée de récupération.
3. Ajouter les infos au dictionnaire récupéré.
4. Pour les clients informés de maggot, vous pouvez désormais vérifier que le SHA1 est correct.
5. Écrire le fichier torrent récupéré.


## Discussion

En utilisant la méthode décrite ci-dessus, l'augmentation de taille du torrent est très petite, typiquement de 200 à 500 octets. Robert va livrer avec la nouvelle création d'entrée du dictionnaire info, et il ne sera pas possible de la désactiver. Voici la structure :

```
dictionnaire principal {
    Chaînes de trackers, commentaires, etc.
    info : {
        dictionnaire principal encodé en B compressé sans le dictionnaire info et toutes les autres infos habituelles
    }
}
```
