---
title: "Améliorations du Transport IPv6"
number: "158"
author: "zzz, original"
created: "2021-03-19"
lastupdated: "2021-04-26"
status: "Fermé"
thread: "http://zzz.i2p/topics/3060"
target: "0.9.50"
---

## Remarque
Déploiement et test du réseau en cours.
Sujette à de légères révisions.


## Aperçu

Cette proposition vise à mettre en œuvre des améliorations pour les transports SSU et NTCP2 concernant IPv6.


## Motivation

Avec la croissance d'IPv6 dans le monde et les configurations uniquement IPv6 (en particulier sur mobile) devenant plus courantes,
nous devons améliorer notre prise en charge d'IPv6 et éliminer les hypothèses selon lesquelles
tous les routeurs sont compatibles IPv4.


### Vérification de la Connectivité

Lors de la sélection de pairs pour des tunnels, ou lors de la sélection des chemins OBEP/IBGW pour l'acheminement des messages,
il est utile de calculer si le routeur A peut se connecter au routeur B.
En général, cela signifie déterminer si A a une capacité sortante pour un type de transport et d'adresse (IPv4/v6)
qui correspond à l'une des adresses entrantes annoncées de B.

Cependant, dans de nombreux cas, nous ne connaissons pas les capacités de A et devons faire des suppositions.
Si A est caché ou protégé par un pare-feu, les adresses ne sont pas publiées, et nous n'avons pas de connaissance directe -
nous supposons donc qu'il est compatible IPv4, et non compatible IPv6.
La solution consiste à ajouter deux nouvelles "caps" ou capacités aux Informations de Routeur pour indiquer la capacité sortante pour IPv4 et IPv6.


### Initiateurs IPv6

Nos spécifications [SSU](/en/docs/transport/ssu/) et [SSU-SPEC](/en/docs/spec/ssu/) contiennent des erreurs et des incohérences concernant le support
des initiateurs IPv6 pour les introductions IPv4.
Dans tous les cas, cela n'a jamais été mis en œuvre dans I2P Java ou i2pd.
Cela doit être corrigé.


### Introductions IPv6

Nos spécifications [SSU](/en/docs/transport/ssu/) et [SSU-SPEC](/en/docs/spec/ssu/) indiquent clairement que
les introductions IPv6 ne sont pas prises en charge.
Cela était basé sur l'hypothèse qu'IPv6 n'est jamais derrière un pare-feu.
Cela est clairement faux, et nous devons améliorer le support pour les routeurs IPv6 derrière un pare-feu.


### Diagrammes d'Introduction

Légende : ----- est IPv4, ====== est IPv6

Actuel IPv4 uniquement :

```
      Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```


Introduction IPv4, initiateur IPv6

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```

Introduction IPv6, initiateur IPv6


```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```

Introduction IPv6, initiateur IPv4

```
Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```


## Conception

Trois changements doivent être mis en œuvre.

- Ajouter les capacités "4" et "6" aux capacités d'Adresse de Routeur pour indiquer le support sortant IPv4 et IPv6
- Ajouter le support des introductions IPv4 via des initiateurs IPv6
- Ajouter le support des introductions IPv6 via des initiateurs IPv4 et IPv6



## Spécification

### Caps 4/6

Cela a été initialement mis en œuvre sans proposition formelle, mais c'est requis pour
les introductions IPv6, nous l'incluons donc ici.
Voir aussi [CAPS](http://zzz.i2p/topics/3050).


Deux nouvelles capacités "4" et "6" sont définies.
Ces nouvelles capacités seront ajoutées à la propriété "caps" dans l'Adresse de Routeur, pas dans les caps d'Informations de Routeur.
Nous n'avons actuellement pas de propriété "caps" définie pour NTCP2.
Une adresse SSU avec initiateurs est, par définition, actuellement ipv4. Nous ne supportons pas du tout l'introduction ipv6.
Cependant, cette proposition est compatible avec les introductions IPv6. Voir ci-dessous.

De plus, un routeur peut supporter la connectivité via un réseau de superposition tel qu'I2P-sur-Yggdrasil,
mais ne souhaite pas publier d'adresse, ou cette adresse n'a pas un format IPv4 ou IPv6 standard.
Ce nouveau système de capacités doit être suffisamment flexible pour supporter ces réseaux également.

Nous définissons les changements suivants :

NTCP2 : Ajouter la propriété "caps"

SSU : Ajouter le support pour une Adresse de Routeur sans hôte ni initiateurs, pour indiquer un support sortant
pour IPv4, IPv6, ou les deux.

Les deux transports : Définir les valeurs de caps suivantes :

- "4" : support IPv4
- "6" : support IPv6

Plusieurs valeurs peuvent être prises en charge dans une seule adresse. Voir ci-dessous.
Au moins une de ces caps est obligatoire si aucune valeur "hôte" n'est incluse dans l'Adresse de Routeur.
Au plus une de ces caps est facultative si une valeur "hôte" est incluse dans l'Adresse de Routeur.
Des capacités de transport supplémentaires peuvent être définies à l'avenir pour indiquer le support pour les réseaux de superposition ou d'autres connectivités.


#### Cas d'utilisation et exemples

SSU :

SSU avec hôte : 4/6 optionnel, jamais plus d'un.
Exemple : SSU caps="4" host="1.2.3.4" key=... port="1234"

SSU uniquement sortant pour un, autre est publié : Caps uniquement, 4/6.
Exemple : SSU caps="6"

SSU avec initiateurs : jamais combiné. 4 ou 6 est requis.
Exemple : SSU caps="4" iexp0=... ihost0=... iport0=... itag0=... key=...

SSU caché : Caps uniquement, 4, 6, ou 46. Multiple est autorisé.
Pas besoin de deux adresses, une avec 4 et une avec 6.
Exemple : SSU caps="46"

NTCP2 :

NTCP2 avec hôte : 4/6 optionnel, jamais plus d'un.
Exemple : NTCP2 caps="4" host="1.2.3.4" i=... port="1234" s=... v="2"

NTCP2 uniquement sortant pour un, autre est publié : Caps, s, v uniquement, 4/6/y, multiple est autorisé.
Exemple : NTCP2 caps="6" i=... s=... v="2"

NTCP2 caché : Caps, s, v uniquement 4/6, multiple est autorisé. Pas besoin de deux adresses, une avec 4 et une avec 6.
Exemple : NTCP2 caps="46" i=... s=... v="2"



### Initiateurs IPv6 pour IPv4

Les changements suivants sont nécessaires pour corriger les erreurs et incohérences dans les spécifications.
Nous avons également décrit cela comme "partie 1" de la proposition.

#### Changements de Spécifications

[SSU](/en/docs/transport/ssu/) indique actuellement (notes IPv6) :

IPv6 est pris en charge depuis la version 0.9.8. Les adresses de relais publiées peuvent être IPv4 ou IPv6, et la communication Alice-Bob peut se faire via IPv4 ou IPv6.

Ajouter ce qui suit :

Bien que la spécification ait été modifiée depuis la version 0.9.8, la communication Alice-Bob via IPv6 n'était pas réellement prise en charge jusqu'à la version 0.9.50.
Les versions antérieures des routeurs Java publiaient à tort la capacité 'C' pour les adresses IPv6,
même s'ils n'agissaient pas réellement comme un initiateur via IPv6.
Par conséquent, les routeurs ne doivent faire confiance à la capacité 'C' d'une adresse IPv6 que si la version du routeur est 0.9.50 ou supérieure.



[SSU-SPEC](/en/docs/spec/ssu/) indique actuellement (Demande de Relais) :

L'adresse IP est uniquement incluse si elle est différente de l'adresse source du paquet et du port.
Dans l'implémentation actuelle, la longueur de l'IP est toujours 0 et le port est toujours 0,
et le récepteur doit utiliser l'adresse source et le port du paquet.
Ce message peut être envoyé via IPv4 ou IPv6. Si IPv6, Alice doit inclure son adresse IPv4 et son port.

Ajouter ce qui suit :

L'IP et le port doivent être inclus pour introduire une adresse IPv4 lors de l'envoi de ce message via IPv6.
Cela est pris en charge à partir de la version 0.9.50.



### Introductions IPv6

Les trois messages de relais SSU (RelayRequest, RelayResponse, et RelayIntro) contiennent des champs de longueur IP
pour indiquer la longueur de l'adresse IP (Alice, Bob, ou Charlie) qui suivra.

Par conséquent, aucun changement au format des messages n'est requis.
Seuls des changements textuels aux spécifications, indiquant que des adresses IP de 16 octets sont autorisées.

Les changements suivants sont nécessaires pour les spécifications.
Nous avons également décrit cela comme "partie 2" de la proposition.


#### Changements de Spécifications

[SSU](/en/docs/transport/ssu/) indique actuellement (notes IPv6) :

La communication Bob-Charlie et Alice-Charlie se fait uniquement via IPv4.

[SSU-SPEC](/en/docs/spec/ssu/) indique actuellement (Demande de Relais) :

Il n'est pas prévu de mettre en œuvre le relais pour IPv6.

Changer pour dire :

Le relais pour IPv6 est pris en charge à partir de la version 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) indique actuellement (Réponse de Relais) :

L'adresse IP de Charlie doit être IPv4, car c'est l'adresse à laquelle Alice enverra la SessionRequest après le Hole Punch.
Il n'est pas prévu de mettre en œuvre le relais pour IPv6.

Changer pour dire :

L'adresse IP de Charlie peut être IPv4 ou, à partir de la version 0.9.xx, IPv6.
C'est l'adresse à laquelle Alice enverra la SessionRequest après le Hole Punch.
Le relais pour IPv6 est pris en charge à partir de la version 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) indique actuellement (Introduction de Relais) :

L'adresse IP d'Alice est toujours de 4 octets dans l'implémentation actuelle, car Alice essaie de se connecter à Charlie via IPv4.
Ce message doit être envoyé via une connexion IPv4 établie,
car c'est le seul moyen pour Bob de connaître l'adresse IPv4 de Charlie à renvoyer à Alice dans la Réponse de Relais.

Changer pour dire :

Pour IPv4, l'adresse IP d'Alice est toujours de 4 octets, car Alice essaie de se connecter à Charlie via IPv4.
À partir de la version 0.9.xx, IPv6 est pris en charge, et l'adresse IP d'Alice peut être de 16 octets.

Pour IPv4, ce message doit être envoyé via une connexion IPv4 établie,
car c'est le seul moyen pour Bob de connaître l'adresse IPv4 de Charlie à renvoyer à Alice dans la Réponse de Relais.
À partir de la version 0.9.xx, IPv6 est pris en charge, et ce message peut être envoyé via une connexion IPv6 établie.

Ajouter aussi :

À partir de la version 0.9.xx, toute adresse SSU publiée avec des initiateurs doit contenir "4" ou "6" dans l'option "caps".


## Migration

Tous les anciens routeurs devraient ignorer la propriété caps dans NTCP2, et les caractères inconnus de capacité dans la propriété caps SSU.

Toute adresse SSU avec initiateurs qui ne contient pas un cap "4" ou "6" est supposée être pour une introduction IPv4.
