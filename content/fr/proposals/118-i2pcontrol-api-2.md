---
title: "API I2PControl 2"
number: "118"
author: "hottuna"
created: "23-01-2016"
lastupdated: "22-03-2018"
status: "Rejeté"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## Aperçu

Cette proposition décrit API2 pour I2PControl.

Cette proposition a été rejetée et ne sera pas mise en œuvre, car elle rompt la compatibilité ascendante. Voir le lien du fil de discussion pour plus de détails.

### Avertissement pour les développeurs !

Tous les paramètres RPC seront désormais en minuscules. Cela *va* briser la compatibilité ascendante avec les implémentations API1. La raison en est de fournir aux utilisateurs de >=API2 l'API la plus simple et la plus cohérente possible.


## Spécification API 2

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### Paramètres

**`"id"`**

Le numéro d'identification de la requête. Utilisé pour identifier quelle réponse a été engendrée par quelle requête.

**`"method_name"`**

Le nom du RPC qui est invoqué.

**`"auth_token"`**

Le jeton d'authentification de session. Doit être fourni avec chaque RPC, sauf pour l'appel 'authenticate'.

**`"method_parameter_value"`**

Le paramètre de la méthode. Utilisé pour offrir différentes variantes d'une méthode, comme 'get', 'set' et autres variantes de ce type.

**`"result_value"`**

La valeur que retourne le RPC. Son type et son contenu dépendent de la méthode et de la méthode spécifique.


### Préfixes

La méthode de naming des RPC est similaire à celle utilisée en CSS, avec des préfixes de vendeur pour les différentes implémentations d'API (i2p, kovri, i2pd):

```text
XXX.YYY.ZZZ
    i2p.XXX.YYY.ZZZ
    i2pd.XXX.YYY.ZZZ
    kovri.XXX.YYY.ZZZ
```

L'idée générale des préfixes spécifiques aux vendeurs est de permettre une certaine flexibilité et de laisser les implémentations innover sans avoir à attendre que chaque autre implémentation rattrape son retard. Si un RPC est implémenté par toutes les implémentations, ses multiples préfixes peuvent être supprimés et il peut être inclus comme un RPC central dans la prochaine version de l'API.


### Guide de lecture des méthodes

 * **rpc.method**

   * *paramètre* [type de paramètre] : [null], [number], [string], [boolean],
     [array] ou [object]. [object] étant une carte {clé:valeur}.

Renvoie:
```text

  "return_value" [string] // C'est la valeur retournée par l'appel RPC
```


### Méthodes

* **authenticate** - Étant donné qu'un mot de passe correct est fourni, cette méthode vous fournit un jeton pour un accès supplémentaire et une liste des niveaux d'API pris en charge.

  * *password* [string] : Le mot de passe pour cette implémentation i2pcontrol

    Renvoie:
```text
    [object]
    {
      "token" : [string], // Le jeton à utiliser devra être fourni avec toutes les autres méthodes RPC
      "api" : [[int],[int], ...]  // Une liste des niveaux d'API pris en charge.
    }
```

* **control.** - Contrôler i2p

  * **control.reseed** - Commencer le réensemencement

    * [nil] : Aucun paramètre nécessaire

    Renvoie:
```text
      [nil]
```

  * **control.restart** - Redémarrer l'instance i2p

    * [nil] : Aucun paramètre nécessaire

    Renvoie:
```text
      [nil]
```

  * **control.restart.graceful** - Redémarrer l'instance i2p en douceur

    * [nil] : Aucun paramètre nécessaire

    Renvoie:
```text
      [nil]
```

  * **control.shutdown** - Éteindre l'instance i2p

    * [nil] : Aucun paramètre nécessaire

    Renvoie:
```text
      [nil]
```

  * **control.shutdown.graceful** - Éteindre l'instance i2p en douceur

    * [nil] : Aucun paramètre nécessaire

    Renvoie:
```text
      [nil]
```

  * **control.update.find** - **BLOQUANT** Recherche des mises à jour signées

    * [nil] : Aucun paramètre nécessaire

    Renvoie:
```text
      true [boolean] // True si et seulement si une mise à jour signée est disponible
```

  * **control.update.start** - Lancer le processus de mise à jour

    * [nil] : Aucun paramètre nécessaire

    Renvoie:
```text
      [nil]
```

* **i2pcontrol.** - Configurer i2pcontrol

  * **i2pcontrol.address** - Obtenir/Configurer l'adresse IP à laquelle i2pcontrol écoute.

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      "0.0.0.0" [string]
```

    * *set* [string] : Ce sera une adresse IP comme "0.0.0.0" ou "192.168.0.1"

    Renvoie:
```text
      [nil]
```

  * **i2pcontrol.password** - Changer le mot de passe i2pcontrol.

    * *set* [string] : Définir le nouveau mot de passe sur cette chaîne

    Renvoie:
```text
      [nil]
```

  * **i2pcontrol.port** - Obtenir/Configurer le port sur lequel i2pcontrol écoute.

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      7650 [number]
```

    * *set* [number] : Changer le port sur lequel i2pcontrol écoute pour ce port

    Renvoie:
```text
      [nil]
```

* **settings.** - Obtenir/Configurer les paramètres de l'instance i2p

  * **settings.advanced** - Paramètres avancés

    * *get*  [string] : Obtenir la valeur de ce paramètre

    Renvoie:
```text
      "setting-value" [string]
```

    * *getAll* [null] :

    Renvoie:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string] : Définir la valeur de ce paramètre
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    Renvoie:
```text
      [nil]
```

  * **settings.bandwidth.in** - Paramètres de la bande passante entrante
  * **settings.bandwidth.out** - Paramètres de la bande passante sortante

    * *get* [nil] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      0 [number]
```

    * *set* [number] : Définir la limite de bande passante

    Renvoie:
```text
     [nil]
```

  * **settings.ntcp.autoip** - Obtenir le paramètre de détection automatique de l'IP pour NTCP

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - Obtenir le nom d'hôte NTCP

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      "0.0.0.0" [string]
```

    * *set* [string] : Définir le nouveau nom d'hôte

    Renvoie:
```text
      [nil]
```

  * **settings.ntcp.port** - Port NTCP

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      0 [number]
```

    * *set* [number] : Définir le nouveau port NTCP.

    Renvoie:
```text
      [nil]
```

    * *set* [boolean] : Définir la détection automatique de l'IP NTCP

    Renvoie:
```text
      [nil]
```

  * **settings.ssu.autoip** - Configurer le paramètre de détection automatique de l'IP pour SSU

    * *get* [nil] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - Configurer le nom d'hôte SSU

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      "0.0.0.0" [string]
```

    * *set* [string] : Définir le nouveau nom d'hôte SSU

    Renvoie:
```text
      [nil]
```

  * **settings.ssu.port** - Port SSU

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      0 [number]
```

    * *set* [number] : Définir le nouveau port SSU.

    Renvoie:
```text
      [nil]
```

    * *set* [boolean] : Définir la détection automatique de l'IP SSU

    Renvoie:
```text
      [nil]
```

  * **settings.share** - Obtenir le pourcentage de partage de la bande passante

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      0 [number] // Pourcentage de partage de bande passante (0-100)
```

    * *set* [number] : Définir le pourcentage de partage de bande passante (0-100)

    Renvoie:
```text
      [nil]
```

  * **settings.upnp** - Activer ou désactiver UPNP

    * *get* [nil] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      true [boolean]
```

    * *set* [boolean] : Définir la détection automatique de l'IP SSU

    Renvoie:
```text
      [nil]
```

* **stats.** - Obtenir les statistiques de l'instance i2p

  * **stats.advanced** - Cette méthode donne accès à toutes les statistiques conservées dans l'instance.

    * *get* [string] : Nom de la statistique avancée à fournir
    * *Optionnel:* *period* [number] : La période pour la statistique demandée

  * **stats.knownpeers** - Retourne le nombre de pairs connus
  * **stats.uptime** - Retourne le temps en ms depuis le démarrage du routeur
  * **stats.bandwidth.in** - Retourne la bande passante entrante (idéalement pour la dernière seconde)
  * **stats.bandwidth.in.total** - Retourne le nombre d'octets reçus depuis le dernier redémarrage
  * **stats.bandwidth.out** - Retourne la bande passante sortante (idéalement pour la dernière seconde)
  * **stats.bandwidth.out.total** - Retourne le nombre d'octets envoyés depuis le dernier redémarrage
  * **stats.tunnels.participating** - Retourne le nombre de tunnels actuellement impliqués
  * **stats.netdb.peers.active** - Retourne le nombre de pairs avec lesquels nous avons récemment communiqué
  * **stats.netdb.peers.fast** - Retourne le nombre de pairs "rapides"
  * **stats.netdb.peers.highcapacity** - Retourne le nombre de pairs "haute capacité"
  * **stats.netdb.peers.known** - Retourne le nombre de pairs connus

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      0.0 [number]
```

* **status.** - Obtenir le statut de l'instance i2p

  * **status.router** - Obtenir le statut du routeur

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      "status" [string]
```

  * **status.net** - Obtenir le statut du réseau du routeur

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTING
       *    2 – FIREWALLED
       *    3 – HIDDEN
       *    4 – WARN_FIREWALLED_AND_FAST
       *    5 – WARN_FIREWALLED_AND_FLOODFILL
       *    6 – WARN_FIREWALLED_WITH_INBOUND_TCP
       *    7 – WARN_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERROR_I2CP
       *    9 – ERROR_CLOCK_SKEW
       *   10 – ERROR_PRIVATE_TCP_ADDRESS
       *   11 – ERROR_SYMMETRIC_NAT
       *   12 – ERROR_UDP_PORT_IN_USE
       *   13 – ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
       *   14 – ERROR_UDP_DISABLED_AND_TCP_UNSET
       */
```

  * **status.isfloodfill** - L'instance i2p est-elle actuellement une floodfill

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      true [boolean]
```

  * **status.isreseeding** - L'instance i2p est-elle actuellement en train de réensemencer

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      true [boolean]
```

  * **status.ip** - IP publique détectée de cette instance i2p

    * *get* [null] : Ce paramètre n'a pas besoin d'être défini.

    Renvoie:
```text
      "0.0.0.0" [string]
```
