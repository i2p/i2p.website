---
title: "Spécification de mise à jour logicielle"
description: "Spécification pour le mécanisme de mise à jour logicielle I2P, le format de fichier SU3, et le flux d'actualités"
slug: "updates"
aliases:
  - "/fr/updates"
  - "/fr/updates/"
category: "Conception"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## Vue d'ensemble

I2P utilise un système simple mais sécurisé pour la mise à jour automatique des logiciels. La console du router récupère périodiquement un fichier de nouvelles depuis une URL I2P configurable. Il existe une URL de sauvegarde codée en dur pointant vers le site web du projet, au cas où l'hôte de nouvelles du projet par défaut deviendrait indisponible.

Le contenu du fichier de nouvelles est affiché sur la page d'accueil de la console du router. De plus, le fichier de nouvelles contient le numéro de version le plus récent du logiciel. Si la version est supérieure au numéro de version du router, il affichera une indication à l'utilisateur qu'une mise à jour est disponible.

Le router peut optionnellement télécharger, ou télécharger et installer, la nouvelle version s'il est configuré pour le faire.

## Spécification de fichier d'anciennes nouvelles

Ce format est remplacé par le format de nouvelles su3 depuis la version 0.9.17.

Le fichier news.xml peut contenir les éléments suivants :

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
Les paramètres de l'entrée i2p.release sont les suivants. Toutes les clés sont insensibles à la casse. Toutes les valeurs doivent être entre guillemets doubles.

**date** : La date de publication de la version du router. Non utilisé. Format non spécifié.

**minJavaVersion** : La version minimale de Java requise pour exécuter la version actuelle. Depuis la version 0.9.9.

**minVersion** : La version minimale du router requise pour mettre à jour vers la version actuelle. Si un router est plus ancien que cela, l'utilisateur doit (manuellement ?) mettre à jour vers une version intermédiaire en premier. À partir de la version 0.9.9.

**su3Clearnet** : Une ou plusieurs URL HTTP où le fichier de mise à jour .su3 peut être trouvé sur le clearnet (non-I2P). Plusieurs URL doivent être séparées par un espace ou une virgule. Depuis la version 0.9.9.

**su3SSL** : Une ou plusieurs URLs HTTPS où le fichier de mise à jour .su3 peut être trouvé sur le clearnet (non-I2P). Plusieurs URLs doivent être séparées par un espace ou une virgule. Depuis la version 0.9.9.

**sudTorrent** : Le lien magnet pour le torrent .sud (non-pack200) de la mise à jour. Depuis la version 0.9.4.

**su2Torrent** : Le lien magnet pour le torrent .su2 (pack200) de la mise à jour. Depuis la version 0.9.4.

**su3Torrent** : Le lien magnet pour le torrent .su3 (nouveau format) de la mise à jour. Depuis la version 0.9.9.

**version** : Requis. La dernière version actuelle du router disponible.

Les éléments peuvent être inclus dans des commentaires XML pour empêcher l'interprétation par les navigateurs. L'élément i2p.release et la version sont obligatoires. Tous les autres sont optionnels. NOTE : En raison des limitations du parseur, un élément entier doit être sur une seule ligne.

## Spécification de fichier de mise à jour

À partir de la version 0.9.9, le fichier de mise à jour signé, nommé i2pupdate.su3, utilisera le format de fichier "su3" spécifié ci-dessous. Les signataires de version approuvés utiliseront des clés RSA de 4096 bits. Les certificats de clé publique X.509 pour ces signataires sont distribués dans les paquets d'installation du router. Les mises à jour peuvent contenir des certificats pour de nouveaux signataires approuvés, et/ou contenir une liste de certificats à supprimer pour révocation.

## Spécification de l'ancien fichier de mise à jour

Ce format est obsolète depuis la version 0.9.9.

Le fichier de mise à jour signé, traditionnellement nommé i2pupdate.sud, est simplement un fichier zip avec un en-tête de 56 octets ajouté au début. L'en-tête contient :

- Une [Signature](/docs/specs/common-structures#signature) DSA de 40 octets
- Une version I2P de 16 octets en UTF-8, complétée avec des zéros de fin si nécessaire

La signature ne couvre que l'archive zip - pas la version préfixée. La signature doit correspondre à l'une des clés DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) configurées dans le router, qui possède une liste codée en dur par défaut des clés des gestionnaires de version actuels du projet.

À des fins de comparaison de versions, les champs de version contiennent [0-9]*, les séparateurs de champs sont '-', '_', et '.', et tous les autres caractères sont ignorés.

À partir de la version 0.8.8, la version doit également être spécifiée comme commentaire du fichier zip en UTF-8, sans les zéros de fin. Le router de mise à jour vérifie que la version dans l'en-tête (non couverte par la signature) correspond à la version dans le commentaire du fichier zip, qui est couverte par la signature. Ceci empêche l'usurpation du numéro de version dans l'en-tête.

## Téléchargement et Installation

Le router télécharge d'abord l'en-tête du fichier de mise à jour depuis l'une des URL I2P d'une liste configurable, en utilisant le client HTTP intégré et le proxy, et vérifie que la version est plus récente. Cela évite le problème des hôtes de mise à jour qui n'ont pas le fichier le plus récent. Le router télécharge ensuite le fichier de mise à jour complet. Le router vérifie que la version du fichier de mise à jour est plus récente avant l'installation. Il vérifie aussi, bien sûr, la signature, et vérifie que le commentaire du fichier zip correspond à la version de l'en-tête, comme expliqué ci-dessus.

Le fichier zip est extrait et copié vers "i2pupdate.zip" dans le répertoire de configuration I2P (~/.i2p sous Linux).

Depuis la version 0.7.12, le router prend en charge la décompression Pack200. Les fichiers à l'intérieur de l'archive zip avec un suffixe .jar.pack ou .war.pack sont décompressés de manière transparente vers un fichier .jar ou .war. Les fichiers de mise à jour contenant des fichiers .pack sont traditionnellement nommés avec un suffixe '.su2'. Pack200 réduit les fichiers de mise à jour d'environ 60%.

À partir de la version 0.8.7, le router supprimera les fichiers libjbigi.so et libjcpuid.so si l'archive zip contient un fichier lib/jbigi.jar, afin que les nouveaux fichiers soient extraits de jbigi.jar.

À partir de la version 0.8.12, si l'archive zip contient un fichier deletelist.txt, le router supprimera les fichiers qui y sont listés. Le format est :

- Un nom de fichier par ligne
- Tous les noms de fichiers sont relatifs au répertoire d'installation ; aucun nom de fichier absolu autorisé, aucun fichier commençant par ".."
- Les commentaires commencent par '#'

Le router supprimera alors le fichier deletelist.txt.

## Spécification du fichier SU3

Cette spécification est utilisée pour les mises à jour du router depuis la version 0.9.9, les données de reseed depuis la version 0.9.14, les plugins depuis la version 0.9.15, et le fichier de nouvelles depuis la version 0.9.17.

### Problèmes avec le format .sud/.su2 précédent

- Aucun nombre magique ou drapeaux
- Aucun moyen de spécifier la compression, pack200 ou non, ou l'algorithme de signature
- La version n'est pas couverte par la signature, elle est donc appliquée en exigeant qu'elle soit dans le commentaire du fichier zip (pour les fichiers router) ou dans le fichier plugin.config (pour les plugins)
- Signataire non spécifié donc le vérificateur doit essayer toutes les clés connues
- Le format signature-avant-données nécessite deux passes pour générer le fichier

### Objectifs

- Corriger les problèmes ci-dessus
- Migrer vers un algorithme de signature plus sécurisé
- Conserver les informations de version dans le même format et décalage pour la compatibilité avec les vérificateurs de version existants
- Vérification de signature et extraction de fichier en une seule passe

### Spécification

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
Tous les champs inutilisés doivent être définis à 0 pour la compatibilité avec les versions futures.

### Détails de la signature

La signature couvre l'intégralité de l'en-tête en commençant à l'octet 0, jusqu'à la fin du contenu. Nous utilisons des signatures brutes. Calculez le hash des données (en utilisant le type de hash impliqué par le type de signature aux octets 8-9) et transmettez-le à une fonction de signature ou de vérification "brute" (par exemple "NONEwithRSA" en Java).

Bien que la vérification de signature et l'extraction de contenu puissent être implémentées en une seule passe, une implémentation doit lire et mettre en mémoire tampon les 10 premiers octets pour déterminer le type de hachage avant de commencer la vérification.

Les longueurs de signature pour les différents types de signature sont données dans la spécification [Signature](/docs/specs/common-structures#signature). Complétez la signature avec des zéros en tête si nécessaire. Voir la [page des détails cryptographiques](/docs/specs/cryptography#sig) pour les paramètres des différents types de signature.

### Notes

Le type de contenu spécifie le domaine de confiance. Pour chaque type de contenu, les clients maintiennent un ensemble de certificats de clés publiques X.509 pour les parties autorisées à signer ce contenu. Seuls les certificats pour le type de contenu spécifié peuvent être utilisés. Le certificat est recherché par l'ID du signataire. Les clients doivent vérifier que le type de contenu correspond à celui attendu pour l'application.

Toutes les valeurs sont dans l'ordre des octets réseau (big endian).

Pour une implémentation Python des signatures RSA brutes compatibles avec Java "NONEwithRSA", voir [cet article Stack Overflow](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530).

## Spécification du fichier de mise à jour SU3 du router

### Détails SU3

- Type de contenu SU3 : 1 (ROUTER UPDATE)
- Type de fichier SU3 : 0 (ZIP)
- Version SU3 : La version du router

Les fichiers jar et war dans le zip ne sont plus compressés avec pack200 comme documenté ci-dessus pour les fichiers "su2", car les environnements d'exécution Java récents ne le prennent plus en charge.

### Notes

- Pour les versions de release, la version SU3 est la version "de base" du router, par exemple "0.9.20".
- Pour les builds de développement, qui sont supportés depuis la release 0.9.20, la version SU3 est la version "complète" du router, par exemple "0.9.20-5" ou "0.9.20-5-rc". Voir RouterVersion.java dans le [code source I2P](https://github.com/i2p/i2p.i2p).

## Spécification du fichier de reseed SU3

Depuis la version 0.9.14, les données de reseed sont livrées dans un format de fichier "su3".

### Objectifs

- Fichiers signés avec des signatures fortes et des certificats de confiance pour empêcher les attaques de l'homme du milieu qui pourraient démarrer les victimes dans un réseau séparé et non fiable.
- Utiliser le format de fichier su3 déjà utilisé pour les mises à jour et les plugins
- Fichier compressé unique pour accélérer le reseeding, qui était lent à récupérer 200 fichiers

### Spécification

1. Le fichier doit être nommé "i2pseeds.su3". À partir de la version 0.9.42, le demandeur devrait ajouter une chaîne de requête "?netid=2" à l'URL de la requête, en supposant l'ID de réseau actuel de 2. Cela peut être utilisé pour empêcher les connexions inter-réseaux. Les réseaux de test devraient définir un ID de réseau différent. Voir la proposition 147 pour plus de détails.
2. Le fichier doit se trouver dans le même répertoire que les router infos sur le serveur web.
3. Un router tentera d'abord de récupérer (URL d'index)/i2pseeds.su3 ; si cela échoue, il récupérera l'URL d'index puis récupérera les fichiers router info individuels trouvés dans les liens.

### Détails SU3

- Type de contenu SU3 : 3 (RESEED)
- Type de fichier SU3 : 0 (ZIP)
- Version SU3 : Secondes depuis l'époque, en ASCII (date +%s). Ne revient PAS à zéro en 2038 ou 2106.
- Les fichiers d'informations de router dans le fichier zip doivent être au "niveau supérieur". Aucun répertoire n'est présent dans le fichier zip.
- Les fichiers d'informations de router doivent être nommés "routerInfo-(hash de router base 64 de 44 caractères).dat", comme dans l'ancien mécanisme de reseed. L'alphabet base 64 I2P doit être utilisé.

### Notes

- Avertissement : Plusieurs reseeds sont connus pour ne pas répondre via IPv6. Il est recommandé de forcer ou de privilégier IPv4.
- Avertissement : Certains reseeds utilisent des certificats CA auto-signés. Les implémentations doivent soit importer et faire confiance à ces CA lors du reseed, soit omettre les reseeds auto-signés de la liste de reseed.
- Les clés de signature reseed sont distribuées aux implémentations sous forme de certificats X.509 auto-signés avec des clés RSA-4096 (type de signature 6). Les implémentations devraient faire respecter les dates de validité dans les certificats.

## Spécification du fichier de plugin SU3

À partir de la version 0.9.15, les plugins peuvent être empaquetés dans un format de fichier "su3".

### Détails SU3

- Type de contenu SU3 : 2 (PLUGIN)
- Type de fichier SU3 : 0 (ZIP) - Voir la [spécification des plugins](/docs/specs/plugin) pour plus de détails.
- Version SU3 : La version du plugin, doit correspondre à celle dans plugin.config.

Les fichiers jar et war dans le zip ne doivent pas être compressés avec pack200 comme documenté ci-dessus pour les fichiers "su2", car les versions récentes de Java ne le prennent plus en charge.

## Spécification du fichier de nouvelles SU3

À partir de la version 0.9.17, les nouvelles sont délivrées dans un format de fichier « su3 ».

### Objectifs

- Actualités signées avec des signatures fortes et des certificats de confiance
- Utilise le format de fichier su3 déjà utilisé pour les mises à jour, le reseeding et les plugins
- Format XML standard pour utilisation avec des analyseurs standards
- Format Atom standard pour utilisation avec des lecteurs et générateurs de flux standards
- Assainissement et vérification du HTML avant affichage sur la console
- Adapté pour une implémentation facile sur Android et autres plateformes sans console HTML

### Détails SU3

- Type de contenu SU3 : 4 (NEWS)
- Type de fichier SU3 : 1 (XML) ou 3 (XML.GZ)
- Version SU3 : Secondes depuis l'époque, en ASCII (date +%s). Ne repart PAS à zéro en 2038 ou 2106.
- Format de fichier : XML ou XML compressé avec gzip, contenant un flux XML [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom). Le jeu de caractères doit être UTF-8.

### Détails du flux Atom

Les éléments `<feed>` suivants sont utilisés :

**`<entry>`** : Un élément de nouvelles. Voir ci-dessous.

**`<i2p:release>`** : Métadonnées de mise à jour I2P. Voir ci-dessous.

**`<i2p:revocations>`** : Révocations de certificats. Voir ci-dessous.

**`<i2p:blocklist>`** : Données de liste de blocage. Voir ci-dessous.

**`<updated>`** : Requis. Horodatage pour le flux (conforme à la [RFC 4287](https://tools.ietf.org/html/rfc4287) section 3.3 et [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Détails de l'entrée Atom

Chaque `<entry>` Atom dans le flux d'actualités peut être analysée et affichée dans la console du router. Les éléments suivants sont utilisés :

**`<author>`** : Optionnel. Contenant `<name>` - Le nom de l'auteur de l'entrée.

**`<content>`** : Requis. Contenu, doit être type="xhtml". Le XHTML sera assaini avec une liste blanche d'éléments autorisés et une liste noire d'attributs interdits. Les clients peuvent ignorer un élément, ou l'entrée englobante, ou l'ensemble du flux lorsqu'un élément non autorisé est rencontré.

**`<link>`** : Optionnel. Lien pour plus d'informations.

**`<summary>`** : Optionnel. Résumé court, approprié pour une infobulle.

**`<title>`** : Obligatoire. Titre de l'entrée d'actualité.

**`<updated>`** : Requis. Horodatage pour cette entrée (conforme à la section 3.3 de [RFC 4287](https://tools.ietf.org/html/rfc4287) et à [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Détails de la version Atom i2p:release

Il doit y avoir au moins une entité `<i2p:release>` dans le flux. Chacune contient les attributs et entités suivants :

**date (attribut)** : Obligatoire. Horodatage pour cette entrée (conforme à la [RFC 4287](https://tools.ietf.org/html/rfc4287) section 3.3 et à la [RFC 3339](https://tools.ietf.org/html/rfc3339)). La date peut également être au format tronqué yyyy-mm-dd (sans le 'T') ; il s'agit du format "full-date" dans la RFC 3339. Dans ce format, l'heure est supposée être 00:00:00 UTC pour tout traitement.

**minJavaVersion (attribut)** : Si présent, la version minimale de Java requise pour exécuter la version actuelle.

**minVersion (attribut)** : Si présent, la version minimale du router requise pour mettre à jour vers la version actuelle. Si un router est plus ancien que cela, l'utilisateur doit (manuellement ?) d'abord mettre à jour vers une version intermédiaire.

**`<i2p:version>`** : Requis. La dernière version actuelle du router disponible.

**`<i2p:update>`** : Un fichier de mise à jour (un ou plusieurs). Il doit contenir au moins un élément enfant.   - type (attribut) : "sud", "su2", ou "su3". Doit être unique parmi tous les éléments `<i2p:update>`.   - `<i2p:clearnet>` : Liens de téléchargement direct hors réseau (zéro ou plusieurs). href (attribut) : Un lien http clearnet standard.   - `<i2p:clearnetssl>` : Liens de téléchargement direct hors réseau (zéro ou plusieurs). href (attribut) : Un lien https clearnet standard.   - `<i2p:torrent>` : Lien magnet dans le réseau. href (attribut) : Un lien magnet.   - `<i2p:url>` : Liens de téléchargement direct dans le réseau (zéro ou plusieurs). href (attribut) : Un lien http .i2p dans le réseau.

### Détails des révocations Atom i2p

Cette entité est facultative et il y a au maximum une entité `<i2p:revocations>` dans le flux. Cette fonctionnalité est prise en charge à partir de la version 0.9.26.

L'entité `<i2p:revocations>` contient une ou plusieurs entités `<i2p:crl>`. L'entité `<i2p:crl>` contient les attributs suivants :

**updated (attribut)** : Requis. Horodatage pour cette entrée (conforme à la [RFC 4287](https://tools.ietf.org/html/rfc4287) section 3.3 et [RFC 3339](https://tools.ietf.org/html/rfc3339)). La date peut également être au format tronqué yyyy-mm-dd (sans le 'T') ; c'est le format "full-date" dans la RFC 3339. Dans ce format, l'heure est supposée être 00:00:00 UTC pour tout traitement.

**id (attribut)** : Requis. Un identifiant unique pour le créateur de cette CRL.

**(contenu de l'entité)** : Obligatoire. Une Liste de Révocation de Certificats (CRL) standard encodée en base 64 avec des retours à la ligne, commençant par la ligne '-----BEGIN X509 CRL-----' et se terminant par la ligne '-----END X509 CRL-----'. Voir [RFC 5280](https://tools.ietf.org/html/rfc5280) pour plus d'informations sur les CRL.

### Détails de la blocklist Atom i2p

Cette entité est optionnelle et il y a au maximum une entité `<i2p:blocklist>` dans le flux. Cette fonctionnalité est prévue pour être implémentée dans la version 0.9.28.

L'entité `<i2p:blocklist>` contient une ou plusieurs entités `<i2p:block>` ou `<i2p:unblock>`, une entité "updated", et des attributs "signer" et "sig" :

**signer (attribut)** : Requis. Un identifiant unique (UTF-8) pour la clé publique utilisée pour signer cette liste de blocage.

**sig (attribut)** : Requis. Une signature au format code:b64sig, où code est le numéro de type de signature ASCII, et b64sig est la signature encodée en base 64 (alphabet I2P). Voir ci-dessous pour la spécification des données à signer.

**`<updated>`** : Requis. Horodatage pour la liste de blocage (conforme à la [RFC 4287](https://tools.ietf.org/html/rfc4287) section 3.3 et [RFC 3339](https://tools.ietf.org/html/rfc3339)). La date peut aussi être au format tronqué yyyy-mm-dd (sans le 'T') ; il s'agit du format "full-date" dans la RFC 3339. Dans ce format, l'heure est supposée être 00:00:00 UTC pour tout traitement.

**`<i2p:block>`** : Optionnel, plusieurs entités sont autorisées. Une seule entrée, soit une adresse IPv4 ou IPv6 littérale, soit un hachage de router de 44 caractères en base 64 (alphabet I2P). Les adresses IPv6 peuvent être au format abrégé (contenant "::"). Le support des entrées avec un masque de réseau, par exemple x.y.0.0/16, est optionnel. Le support des noms d'hôte est optionnel.

**`<i2p:unblock>`** : Optionnel, plusieurs entités sont autorisées. Même format que `<i2p:block>`.

**Spécification de signature :** Pour générer les données à signer ou vérifier, concaténez les données suivantes en encodage ASCII : La chaîne mise à jour suivie d'un saut de ligne (ASCII 0x0a), puis chaque entrée de bloc dans l'ordre reçu avec un saut de ligne après chacune, puis chaque entrée de déblocage dans l'ordre reçu avec un saut de ligne après chacune.

## Spécification du fichier de liste de blocage

TBD, non implémenté, voir la proposition 130. Les mises à jour de la liste de blocage sont livrées dans le fichier d'actualités, voir ci-dessus.

## Travail futur

- Le mécanisme de mise à jour du router fait partie de la console web du router. Il n'y a actuellement aucune disposition pour les mises à jour d'un router intégré dépourvu de console router.

## Références

- **[CRYPTO-SIG]** [Cryptographie - Signatures](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [Code source I2P](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Spécification des plugins](/docs/specs/plugin)
- **[Python]** [Signatures RSA brutes en Python](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - Date et heure](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Format de syndication Atom](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Listes de révocation de certificats](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [Type Signature](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [Type SigningPublicKey](/docs/specs/common-structures#signingpublickey)
