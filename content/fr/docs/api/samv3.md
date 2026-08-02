---
title: "SAM V3"
description: "Protocole de messagerie anonyme simple pour les applications I2P non-Java"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM est un protocole client simple permettant d'interagir avec I2P. SAM est le protocole recommandé pour que les applications non-Java se connectent au réseau I2P, et est pris en charge par plusieurs implémentations de routeur. Les applications Java devraient utiliser directement les API de streaming ou I2CP.

La version 3 de SAM a été introduite dans la version 0.7.3 d'I2P (mai 2009) et constitue une interface stable et prise en charge. La version 3.1 est également stable et prend en charge l'option de type de signature, fortement recommandée. Les versions 3.x plus récentes prennent en charge des fonctionnalités avancées. Notez qu'i2pd ne prend actuellement pas en charge la plupart des fonctionnalités des versions 3.2 et 3.3.

Alternatives : [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (obsolète)](/docs/api/bob). Versions obsolètes : [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Bibliothèques SAM connues

Avertissement : Certains peuvent être très anciens ou non supportés. Aucun n'est testé, examiné ou maintenu par le projet I2P, sauf indication contraire ci-dessous. Faites vos propres recherches.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Démarrage rapide

Pour implémenter une application pair-à-pair basique utilisant uniquement TCP, le client doit prendre en charge les commandes suivantes :

- `HELLO VERSION MIN=3.1 MAX=3.1` - Requis pour tous les autres
- `DEST GENERATE SIGNATURE_TYPE=7` - Pour générer notre clé privée et notre destination
- `NAMING LOOKUP NAME=...` - Pour convertir les adresses .i2p en destinations
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - Requis pour STREAM CONNECT et STREAM ACCEPT
- `STREAM CONNECT ID=... DESTINATION=...` - Pour établir des connexions sortantes
- `STREAM ACCEPT ID=...` - Pour accepter les connexions entrantes

## Conseils généraux pour les développeurs

### Conception de l'application

Les sessions SAM (ou, dans I2P, les pools de tunnels ou ensembles de tunnels) sont conçues pour être durables. La plupart des applications n'auront besoin que d'une seule session, créée au démarrage et fermée à la sortie. I2P diffère de Tor, où les circuits peuvent être rapidement créés et abandonnés. Réfléchissez bien et consultez les développeurs d'I2P avant de concevoir votre application pour utiliser plus d'une ou deux sessions simultanées, ou pour créer et supprimer rapidement des sessions. La plupart des modèles de menaces ne nécessiteront pas une session unique pour chaque connexion.

Veuillez également vous assurer que les paramètres de votre application (ainsi que les instructions fournies aux utilisateurs concernant les paramètres du routeur, ou les valeurs par défaut du routeur si vous incluez un routeur) entraînent une contribution de vos utilisateurs en ressources au réseau supérieure à leur consommation. I2P est un réseau pair-à-pair, et le réseau ne pourrait pas survivre si une application populaire provoquait une congestion permanente du réseau.

### Compatibilité et tests

Les implémentations du routeur Java I2P et i2pd sont indépendantes et présentent de légères différences en matière de comportement, de prise en charge des fonctionnalités et de paramètres par défaut. Veuillez tester votre application avec la dernière version des deux routeurs.

i2pd SAM est activé par défaut ; Java I2P SAM ne l'est pas. Fournissez des instructions à vos utilisateurs pour activer SAM dans Java I2P (via /configclients dans la console du routeur), et/ou affichez un message d'erreur clair en cas d'échec de la connexion initiale, par exemple : « assurez-vous que I2P est en cours d'exécution et que l'interface SAM est activée ».

Les routeurs Java I2P et i2pd ont des valeurs par défaut différentes pour la quantité de tunnels. La valeur par défaut de Java I2P est 2 et celle d'i2pd est 5. Pour la plupart des cas avec une bande passante faible à moyenne et un nombre de connexions faible à moyen, 2 ou 3 tunnels sont suffisants. Veuillez spécifier la quantité de tunnels dans le message SESSION CREATE afin d'obtenir des performances cohérentes avec les routeurs Java I2P et i2pd. Voir ci-dessous.

Pour obtenir davantage de conseils destinés aux développeurs afin de garantir que votre application n'utilise que les ressources dont elle a besoin, veuillez consulter [notre guide sur l'intégration d'I2P avec votre application](/docs/applications/embedding).

### Types de signature et de chiffrement

I2P prend en charge plusieurs types de signatures et de chiffrement. Pour des raisons de compatibilité ascendante, SAM utilise par défaut des types anciens et inefficaces, c'est pourquoi tous les clients doivent spécifier des types plus récents.

Le type de signature est spécifié dans les commandes DEST GENERATE et SESSION CREATE (pour les sessions temporaires). Tous les clients doivent définir `SIGNATURE_TYPE=7` (Ed25519).

Le type de chiffrement est spécifié dans la commande SESSION CREATE. Plusieurs types de chiffrement sont autorisés. Les clients doivent définir soit `i2cp.leaseSetEncType=4` (pour ECIES-X25519 uniquement), soit `i2cp.leaseSetEncType=6,4` (pour MLKEM-768 et ECIES-X25519, pour les routeurs prenant en charge l'API 0.9.67 ou supérieure).

## Modifications de la version 3

### Changements de la version 3.0

La version 3.0 a été introduite dans la version 0.7.3 d'I2P. SAM v2 offrait la possibilité de gérer plusieurs sockets sur la même destination I2P *en parallèle*, c'est-à-dire que le client n'avait pas à attendre que des données soient correctement envoyées sur un socket avant d'envoyer des données sur un autre socket. Mais toutes les données transitaient par le même socket client-vers-SAM, ce qui était assez compliqué à gérer pour le client.

SAM v3 gère les sockets différemment : chaque *socket I2P* correspond à un socket unique entre le client et SAM, ce qui est beaucoup plus simple à gérer. Cela ressemble à [BOB](/docs/api/bob).

SAM v3 propose également un port UDP pour envoyer des datagrammes via I2P, et peut renvoyer au serveur de datagrammes du client les datagrammes I2P entrants.

### Changements de la version 3.1

La version 3.1 a été introduite dans la version 0.9.14 de Java I2P (juillet 2014). SAM 3.1 est l'implémentation SAM minimale recommandée en raison de sa prise en charge de types de signatures améliorés par rapport à SAM 3.0. i2pd prend également en charge la plupart des fonctionnalités de la version 3.1.

- DEST GENERATE et SESSION CREATE prennent désormais en charge un paramètre SIGNATURE_TYPE.
- Les paramètres MIN et MAX dans HELLO VERSION sont désormais facultatifs.
- Les paramètres MIN et MAX dans HELLO VERSION prennent désormais en charge les versions à un seul chiffre telles que « 3 ».
- RAW SEND est désormais pris en charge sur la socket de pont.

### Changements de la version 3.2

La version 3.2 a été introduite dans la version 0.9.24 de Java I2P (janvier 2016). Notez qu’i2pd ne prend actuellement pas en charge la plupart des fonctionnalités de la version 3.2.

#### Prise en charge des ports et protocoles I2CP

- Options FROM_PORT et TO_PORT de SESSION CREATE
- Option PROTOCOL de SESSION CREATE avec STYLE=RAW
- Options FROM_PORT et TO_PORT de STREAM CONNECT, DATAGRAM SEND et RAW SEND
- Option PROTOCOL de RAW SEND
- DATAGRAM RECEIVED, RAW RECEIVED, ainsi que les flux et datagrammes répliables transférés ou reçus, incluent FROM_PORT et TO_PORT
- L'option de session RAW HEADER=true entraîne l'ajout en début des datagrammes bruts transférés d'une ligne contenant PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn
- La première ligne des datagrammes envoyés via le port 7655 peut désormais commencer par n'importe quelle version 3.x
- La première ligne des datagrammes envoyés via le port 7655 peut contenir l'une des options FROM_PORT, TO_PORT, PROTOCOL
- RAW RECEIVED inclut PROTOCOL=nnn

#### SSL et authentification

- USER/PASSWORD dans les paramètres HELLO pour l'autorisation. Voir [ci-dessous](#authorization).
- Configuration facultative d'autorisation avec la commande AUTH. Voir [ci-dessous](#authorization-configuration-sam-32-or-higher-optional-feature).
- Prise en charge optionnelle de SSL/TLS sur la socket de contrôle. Voir [ci-dessous](#ssl).
- Option STREAM FORWARD SSL=true

#### Multithreading

- Les ACCEPTs STREAM en attente concurrents sont autorisés sur le même identifiant de session.

#### Analyse de la ligne de commande et maintien de la connexion

- Commandes facultatives QUIT, STOP et EXIT pour fermer la session et la socket. Voir [ci-dessous](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- L'analyse des commandes gère correctement l'UTF-8.
- L'analyse des commandes gère de façon fiable les espaces internes aux guillemets.
- Un antislash « \\ » peut servir à échapper les guillemets en ligne de commande.
- Il est recommandé que le serveur convertisse les commandes en majuscules, pour faciliter les tests via telnet.
- Les valeurs d'options vides comme PROTOCOL ou PROTOCOL= peuvent être autorisées, selon l'implémentation.
- PING/PONG pour le maintien de la connexion (keepalive). Voir ci-dessous.
- Les serveurs peuvent implémenter des délais d'expiration (timeouts) pour la commande HELLO ou pour les commandes suivantes, selon l'implémentation.

### Modifications de la version 3.3

La version 3.3 a été introduite dans la version 0.9.25 de Java I2P (mars 2016). Notez qu'i2pd ne prend actuellement pas en charge la plupart des fonctionnalités de la version 3.3.

- La même session peut être utilisée simultanément pour des flux, des datagrammes et du mode brut. Les paquets et flux entrants seront acheminés selon le protocole I2P et le port de destination. Voir [la section PRIMARY ci-dessous](#sam-primary-sessions-v33-and-higher).
- DATAGRAM SEND et RAW SEND prennent désormais en charge les options SEND_TAGS, TAG_THRESHOLD, EXPIRES et SEND_LEASESET. Voir [la section sur l'envoi de datagrammes ci-dessous](#sending-repliable-or-raw-datagrams).

### Modifications de 2025-04

Deux propositions ont été approuvées et intégrées à la spécification ici en avril 2025. Aucune modification de version n'indique le support. Certaines implémentations ne prennent pas encore en charge ces ajouts, et chez d'autres, le support est préliminaire.

- Prise en charge des datagrammes 2/3 (proposition 163). Spécifié dans SESSION CREATE et SESSION ADD (sous-sessions). Voir ci-dessous.
- Récupération des options de leaseset (proposition 167). Spécifié avec NAMING LOOKUP OPTIONS=true. Voir ci-dessous.

## Protocole version 3

### Spécification de la version 3.3 du protocole SAM (Simple Anonymous Messaging) - Aperçu général

L'application cliente communique avec le pont SAM, qui gère toutes les fonctionnalités I2P (en utilisant la [bibliothèque de streaming](/docs/api/streaming) pour les flux virtuels, ou [I2CP](/docs/protocol/i2cp) directement pour les datagrammes).

Par défaut, la communication entre le client et le pont SAM est ni chiffrée ni authentifiée. Le pont SAM peut prendre en charge des connexions SSL/TLS ; les détails de configuration et d'implémentation ne relèvent pas du champ d'application de cette spécification. À compter de SAM 3.2, des paramètres optionnels d'authentification (nom d'utilisateur/mot de passe) sont pris en charge lors de la poignée de main initiale et peuvent être exigés par le pont.

Les communications I2P peuvent prendre plusieurs formes différentes :

- [Flux virtuels](/docs/api/streaming)
- [Datagrammes répondables et authentifiés](/docs/specs/datagrams#repliable) (messages avec un champ FROM)
- [Datagrammes anonymes](/docs/specs/datagrams#raw) (messages anonymes bruts)
- [Datagram2](/docs/specs/datagrams#datagram2) (un nouveau format répondable et authentifié)
- [Datagram3](/docs/specs/datagrams#datagram3) (un nouveau format répondable mais non authentifié)

Les communications I2P sont prises en charge par des sessions I2P, et chaque session I2P est liée à une adresse (appelée destination). Une session I2P est associée à l'un des trois types ci-dessus, et ne peut pas transporter des communications d'un autre type, sauf en utilisant des [sessions primaires](#sam-primary-sessions-v33-and-higher).

### Encodage et échappement

Tous ces messages SAM sont envoyés sur une seule ligne, terminée par le caractère de nouvelle ligne (\\n). Avant SAM 3.2, seul l'ASCII 7 bits était pris en charge. À partir de SAM 3.2, l'encodage doit être en UTF-8. Toutes les clés ou valeurs encodées en UTF-8 devraient fonctionner.

La mise en forme indiquée dans cette spécification ci-dessous est uniquement destinée à la lisibilité. Bien que les deux premiers mots de chaque message doivent rester dans un ordre précis, l'ordre des paires clé=valeur peut varier (par exemple, « ONE TWO A=B C=D » ou « ONE TWO C=D A=B » sont tous deux des constructions parfaitement valides). En outre, le protocole respecte la casse. Dans ce qui suit, les exemples de messages sont précédés de « -> » pour les messages envoyés par le client au pont SAM, et de « <- » pour les messages envoyés par le pont SAM au client.

La ligne de commande ou de réponse de base prend l'une des formes suivantes :

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
COMMAND sans SUBCOMMAND est pris en charge uniquement pour certaines nouvelles commandes dans SAM 3.2.

Les paires clé=valeur doivent être séparées par un seul espace. (À partir de SAM 3.2, plusieurs espaces sont autorisés.) Les valeurs doivent être entourées de guillemets doubles si elles contiennent des espaces, par exemple : key="longue valeur texte". (Avant SAM 3.2, cela ne fonctionnait pas de manière fiable dans certaines implémentations))

Avant SAM 3.2, il n'existait aucun mécanisme d'échappement. À compter de SAM 3.2, les guillemets doubles peuvent être échappés avec une barre oblique inverse « \\ » et une barre oblique inverse peut être représentée par deux barres obliques inverses « \\\\ ».

### Valeurs vides

À compter de SAM 3.2, les valeurs d'options vides telles que KEY, KEY= ou KEY="" peuvent être autorisées, selon l'implémentation.

### Sensibilité à la casse

Le protocole, tel que spécifié, respecte la casse. Il est recommandé, mais non obligatoire, que le serveur convertisse les commandes en majuscules, afin de faciliter les tests via telnet. Cela permettrait, par exemple, que « hello version » fonctionne. Ceci dépend de l'implémentation. Ne pas convertir les clés ou les valeurs en majuscules, car cela corromprait les options [I2CP](/docs/protocol/i2cp).

### Négociation de connexion SAM

Aucune communication SAM ne peut avoir lieu avant que le client et le pont aient convenu d'une version de protocole, ce qui est réalisé en envoyant par le client un HELLO et par le pont une réponse HELLO REPLY :

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
et

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
À partir de la version 3.1 (I2P 0.9.14), les paramètres MIN et MAX sont facultatifs. SAM retournera toujours la version la plus élevée possible selon les contraintes MIN et MAX, ou la version actuelle du serveur si aucune contrainte n'est fournie.

Si le pont SAM ne peut pas trouver une version appropriée, il répond avec :

```
<- HELLO REPLY RESULT=NOVERSION
```
Si une erreur s'est produite, par exemple un format de requête incorrect, il répond avec :

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

La socket de contrôle du serveur peut éventuellement offrir un support SSL/TLS, tel que configuré sur le serveur et le client. Les implémentations peuvent également proposer d'autres couches de transport ; cela dépasse le cadre de la définition du protocole.

#### Autorisation

Pour l'autorisation, le client ajoute USER="xxx" PASSWORD="yyy" aux paramètres HELLO. Les guillemets doubles pour l'utilisateur et le mot de passe sont recommandés mais pas obligatoires. Un guillemet double à l'intérieur d'un nom d'utilisateur ou d'un mot de passe doit être échappé avec une barre oblique inversée. En cas d'échec, le serveur répondra avec un I2P_ERROR et un message. Il est recommandé d'activer SSL sur tout serveur SAM où une autorisation est requise.

#### Délais d'expiration

Les serveurs peuvent implémenter des délais d'expiration pour la commande HELLO ou pour les commandes ultérieures, selon l'implémentation. Les clients doivent envoyer rapidement la commande HELLO et la commande suivante après la connexion.

Si un délai d'attente expire avant la réception du HELLO, le pont répond par :

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
puis se déconnecte.

Si un délai d'expiration se produit après la réception du HELLO mais avant la commande suivante, le pont répond par :

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
puis se déconnecte.

### Ports et protocole I2CP

Depuis SAM 3.2, les ports et protocoles [I2CP](/docs/protocol/i2cp) peuvent être spécifiés par l'expéditeur client SAM pour être transmis à [I2CP](/docs/protocol/i2cp), et le pont SAM transmettra les informations reçues sur le port et le protocole [I2CP](/docs/protocol/i2cp) au client SAM.

Pour FROM_PORT et TO_PORT, la plage valide est 0-65535, et la valeur par défaut est 0.

Pour PROTOCOL, qui ne peut être spécifié que pour RAW, la plage valide est 0-255, et la valeur par défaut est 18.

Pour les commandes SESSION, les ports et le protocole spécifiés sont les valeurs par défaut pour cette session. Pour les flux ou datagrammes individuels, les ports et le protocole spécifiés remplacent les valeurs par défaut de la session. Pour les flux ou datagrammes reçus, les ports et le protocole indiqués sont ceux reçus via [I2CP](/docs/protocol/i2cp).

#### Différences importantes par rapport à l'IP standard

Les ports I2CP sont destinés aux sockets et datagrammes I2P. Ils n'ont aucun rapport avec vos sockets locaux qui se connectent à SAM.

- Le port 0 est valide et possède une signification particulière.
- Les ports 1 à 1023 ne sont ni spéciaux ni privilégiés.
- Les serveurs écoutent sur le port 0 par défaut, ce qui signifie « tous les ports ».
- Les clients envoient vers le port 0 par défaut, ce qui signifie « n'importe quel port ».
- Les clients envoient depuis le port 0 par défaut, ce qui signifie « non spécifié ».
- Un serveur peut avoir un service à l'écoute sur le port 0 et d'autres services à l'écoute sur des ports supérieurs. Dans ce cas, le service sur le port 0 est celui par défaut, et il sera utilisé si le port de la socket entrante ou du datagramme ne correspond à aucun autre service.
- La plupart des destinations I2P n'exécutent qu'un seul service, vous pouvez donc utiliser les valeurs par défaut et ignorer la configuration des ports I2CP.
- SAM 3.2 ou 3.3 est requis pour spécifier les ports I2CP.
- Si vous n'avez pas besoin de spécifier les ports I2CP, vous n'avez pas besoin de SAM 3.2 ou 3.3 ; SAM 3.1 est suffisant.
- Le protocole 0 est valide et signifie « n'importe quel protocole ». Cette option n'est pas recommandée et ne fonctionnera probablement pas.
- Les sockets I2P sont suivis par un identifiant interne de connexion. Par conséquent, il n'est pas nécessaire que le 5-uplet dest:port:dest:port:protocole soit unique. Par exemple, il peut exister plusieurs sockets avec les mêmes ports entre deux destinations. Les clients n'ont pas besoin de choisir un « port libre » pour une connexion sortante.

Si vous concevez une application SAM 3.3 avec plusieurs sous-sessions, réfléchissez attentivement à la manière d'utiliser efficacement les ports et les protocoles. Consultez la spécification [I2CP](/docs/protocol/i2cp) pour plus d'informations.

### Sessions SAM

Une session SAM est créée lorsqu'un client ouvre une socket vers le pont SAM, effectue un échange de salutation (handshake), puis envoie un message SESSION CREATE. La session se termine lorsque la socket est déconnectée.

Chaque destination I2P enregistrée est associée de manière unique à un identifiant de session (ou surnom). Les identifiants de session, y compris les identifiants de sous-session pour les sessions PRINCIPALES, doivent être globalement uniques sur le serveur SAM. Pour éviter d'éventuelles collisions d'identifiants avec d'autres clients, la meilleure pratique consiste à ce que le client génère ces identifiants aléatoirement.

Chaque session est associée de manière unique à :

- la socket à partir de laquelle le client crée la session
- son ID (ou pseudonyme)

#### Demande de création de session

Le message de création de session ne peut utiliser qu'une seule de ces formes (les messages reçus sous d'autres formes sont répondus par un message d'erreur) :

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION indique quelle destination doit être utilisée pour l'envoi et la réception de messages/flux. La $privkey est la représentation en base 64 de la concaténation de la [Destination](/docs/specs/common-structures#type_Destination), suivie de la [Clé Privée](/docs/specs/common-structures#type_PrivateKey), puis de la [Clé Privée de Signature](/docs/specs/common-structures#type_SigningPrivateKey), éventuellement suivie de la [Signature Hors Ligne](/docs/specs/common-structures#struct_OfflineSignature), ce qui donne 663 octets ou plus en binaire et 884 octets ou plus en base 64, selon le type de signature. Le format binaire est décrit dans le document Fichier de Clé Privée. Voir aussi les remarques complémentaires sur la [Clé Privée](/docs/specs/common-structures#type_PrivateKey) dans la section Génération de Clé de Destination ci-dessous.

Si la clé privée de signature est composée uniquement de zéros, la section [Signature hors ligne](/docs/specs/common-structures#struct_OfflineSignature) suit. Les signatures hors ligne sont uniquement prises en charge pour les sessions STREAM et RAW. Les signatures hors ligne ne peuvent pas être créées avec DESTINATION=TRANSIENT. Le format de la section de signature hors ligne est :

1. Horodatage d'expiration (4 octets, big endian, secondes depuis l'époque, dépassement en 2106)
2. Type de signature de la clé publique de signature temporaire (2 octets, big endian)
3. Clé publique de signature temporaire (longueur spécifiée par le type de signature temporaire)
4. Signature des trois champs ci-dessus par la clé hors ligne (longueur spécifiée par le type de signature de destination)
5. Clé privée de signature temporaire (longueur spécifiée par le type de signature temporaire)

Si la destination est spécifiée comme TRANSITOIRE, le pont SAM crée une nouvelle destination. À partir de la version 3.1 (I2P 0.9.14), si la destination est TRANSITOIRE, un paramètre optionnel SIGNATURE_TYPE est pris en charge. La valeur SIGNATURE_TYPE peut être n'importe quel nom (par exemple ECDSA_SHA256_P256, insensible à la casse) ou nombre (par exemple 1) pris en charge par les [Certificats de clé](/docs/specs/common-structures#type_Certificate). La valeur par défaut est DSA_SHA1, ce qui n'est PAS ce que vous souhaitez. Pour la plupart des applications, veuillez spécifier SIGNATURE_TYPE=7.

$nickname est choisi par le client. Aucun espace n'est autorisé.

Les options supplémentaires fournies sont transmises à la configuration de la session I2P si elles ne sont pas interprétées par le pont SAM (par exemple, outbound.length=0).

Les routeurs Java I2P et i2pd ont des valeurs par défaut différentes pour les quantités de tunnels. La valeur par défaut de Java est 2 et celle d'i2pd est 5. Pour la plupart des cas avec bande passante faible à moyenne et un nombre de connexions faible à moyen, 2 ou 3 tunnels sont suffisants. Veuillez spécifier les quantités de tunnels dans le message SESSION CREATE afin d'obtenir des performances cohérentes avec les routeurs Java I2P et i2pd, en utilisant des options telles que inbound.quantity=3 outbound.quantity=3. Ces options et d'autres [sont documentées dans les liens ci-dessous](#tunnel-i2cp-and-streaming-options).

Le pont SAM devrait déjà être configuré avec le routeur via lequel il doit communiquer sur I2P (bien que, si nécessaire, il puisse exister un moyen de fournir une surcharge, par exemple i2cp.tcp.host=localhost et i2cp.tcp.port=7654).

#### Réponse à la création de session

Après avoir reçu le message de création de session, le pont SAM répondra avec un message d'état de session, comme suit :

Si la création a réussi :

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
Le $privkey est le codage en base 64 de la concaténation de la [Destination](/docs/specs/common-structures#type_Destination), suivie de la [Clé Privée](/docs/specs/common-structures#type_PrivateKey), suivie de la [Clé Privée de Signature](/docs/specs/common-structures#type_SigningPrivateKey), éventuellement suivie de la [Signature Hors Ligne](/docs/specs/common-structures#struct_OfflineSignature), ce qui donne 663 octets ou plus en binaire et 884 octets ou plus en base 64, selon le type de signature. Le format binaire est spécifié dans le fichier de clé privée.

Si le SESSION CREATE contenait une clé privée de signature composée uniquement de zéros et une section [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), la réponse SESSION STATUS inclura les mêmes données dans le même format. Voir la section SESSION CREATE ci-dessus pour plus de détails.

Si le pseudonyme est déjà associé à une session :

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Si la destination est déjà en cours d'utilisation :

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Si la destination n'est pas une clé de destination privée valide :

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Si une autre erreur s'est produite :

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
S'il ne va pas, le MESSAGE doit contenir des informations lisibles par un humain expliquant pourquoi la session n'a pas pu être créée.

Notez que le routeur construit des tunnels avant de répondre avec SESSION STATUS. Cela peut prendre plusieurs secondes, voire une minute ou plus au démarrage du routeur ou en cas de congestion réseau sévère. En cas d'échec, le routeur ne répondra pas avec un message d'erreur pendant plusieurs minutes. Ne définissez pas un délai d'attente court en attendant la réponse. Ne pas abandonner la session pendant la construction des tunnels ni réessayer.

Les sessions SAM vivent et meurent avec la socket à laquelle elles sont associées. Lorsque la socket est fermée, la session prend fin, et toutes les communications utilisant cette session cessent en même temps. Et inversement, lorsque la session se termine pour une raison quelconque, le pont SAM ferme la socket.

### Flux virtuels SAM

Les flux virtuels sont garantis comme étant envoyés de manière fiable et dans l'ordre, avec une notification d'échec ou de réussite dès que celle-ci est disponible.

Les flux sont des sockets de communication bidirectionnels entre deux destinations I2P, mais leur ouverture doit être demandée par l'une d'entre elles. Par la suite, les commandes CONNECT sont utilisées par le client SAM pour effectuer une telle demande. Les commandes FORWARD / ACCEPT sont utilisées par le client SAM lorsqu'il souhaite écouter les demandes provenant d'autres destinations I2P.

### Flux virtuels SAM : CONNECTER

Un client demande une connexion en :

- ouverture d'une nouvelle socket via le pont SAM
- envoi de la même poignée de main HELLO qu'au-dessus
- envoi de la commande STREAM CONNECT

#### Demande de connexion

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Ceci établit une nouvelle connexion virtuelle depuis la session locale dont l'ID est $nickname vers le pair spécifié.

La cible est $destination, qui correspond à la base 64 de la [Destination](/docs/specs/common-structures#type_Destination), soit 516 caractères base 64 ou plus (387 octets ou plus en binaire), selon le type de signature.

**REMARQUE :** Depuis environ 2014 (SAM v3.1), Java I2P prend également en charge les noms d'hôte et les adresses b32 pour le $destination, bien que cela n'ait pas été documenté auparavant. Les noms d'hôte et les adresses b32 sont désormais officiellement pris en charge par Java I2P à compter de la version 0.9.48. Le routeur i2pd prend en charge les noms d'hôte et les adresses b32 à compter de la version 2.38.0 (0.9.50). Pour les deux routeurs, la prise en charge « b32 » inclut également les adresses « b33 » étendues pour les destinations masquées.

#### Réponse de connexion

Si SILENT=true est indiqué, le pont SAM n'émettra aucun autre message sur la socket. Si la connexion échoue, la socket sera fermée. Si la connexion réussit, toutes les données restantes transitant par la socket actuelle sont transférées depuis et vers le destinataire I2P connecté.

Si SILENT=false, ce qui correspond à la valeur par défaut, le pont SAM envoie un dernier message à son client avant de transférer ou de fermer la socket :

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
La valeur de RESULTAT peut être l'une des suivantes :

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
Si le RÉSULTAT est OK, toutes les données restantes transitant par la socket actuelle sont transférées vers et depuis le pair de destination I2P connecté. Si la connexion n'a pas pu être établie (délai d'attente dépassé, etc.), RÉSULTAT contiendra la valeur d'erreur appropriée (accompagnée d'un MESSAGE optionnel en langage humain), et le pont SAM ferme la socket.

Le délai d'expiration interne de la connexion du flux du routeur est d'environ une minute, selon l'implémentation. Ne définissez pas un délai d'attente plus court en attendant la réponse.

### SAM Virtual Streams : ACCEPTER

Un client attend une demande de connexion entrante en :

- ouverture d'une nouvelle socket via le pont SAM
- envoi de la même poignée de main HELLO qu'au-dessus
- envoi de la commande STREAM ACCEPT

#### Accepter la demande

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Cela permet à la session ${nickname} d'écouter une demande de connexion entrante depuis le réseau I2P. ACCEPT n'est pas autorisé lorsqu'il existe un FORWARD actif sur la session.

Depuis SAM 3.2, plusieurs acceptations STREAM en attente simultanées sont autorisées sur le même identifiant de session (même avec le même port). Avant la version 3.2, les acceptations simultanées échouaient avec ALREADY_ACCEPTING. Remarque : Java I2P prend également en charge les acceptations simultanées sur SAM 3.1, à partir de la version 0.9.24 (2016-01). i2pd prend également en charge les acceptations simultanées sur SAM 3.1, à partir de la version 2.50.0 (2023-12).

#### Accepter la réponse

Si SILENT=true est spécifié, le pont SAM n'émettra aucun autre message sur la socket. Si l'acceptation échoue, la socket sera fermée. Si l'acceptation réussit, toutes les données restantes transitant par la socket actuelle sont transférées depuis et vers le pair de destination I2P connecté. Pour plus de fiabilité, et afin de recevoir la destination des connexions entrantes, il est recommandé d'utiliser SILENT=false.

Si SILENT=false, qui est la valeur par défaut, le pont SAM répond avec :

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
La valeur de RESULTAT peut être l'une des suivantes :

```
OK
I2P_ERROR
INVALID_ID
```
Si le résultat n'est pas OK, la socket est immédiatement fermée par le pont SAM. Si le résultat est OK, le pont SAM commence à attendre une demande de connexion entrante provenant d'un autre pair I2P. Lorsqu'une demande arrive, le pont SAM l'accepte et :

Si SILENT=true est indiqué, le pont SAM n'émettra aucun autre message sur la socket cliente. Toutes les données restantes transitant par la socket actuelle sont transférées depuis et vers le pair de destination I2P connecté.

Si SILENT=false a été transmis, ce qui correspond à la valeur par défaut, le pont SAM envoie au client une ligne ASCII contenant la clé publique de destination en base64 du pair demandeur, ainsi que des informations supplémentaires spécifiques à SAM 3.2 uniquement :

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Après cette ligne terminée par '\\n', toutes les données restantes transitant par la socket actuelle sont transférées depuis et vers le pair de destination I2P connecté, jusqu'à ce que l'un des pairs ferme la socket.

#### Erreurs après OK

Dans de rares cas, le pont SAM peut rencontrer une erreur après avoir envoyé RESULT=OK, mais avant qu'une connexion n'arrive et que la ligne $destination soit envoyée au client. Ces erreurs peuvent inclure l'arrêt du routeur, le redémarrage du routeur et la fermeture de la session. Dans ces cas, lorsque SILENT=false, le pont SAM peut, mais n'est pas tenu de (dépend de l'implémentation), envoyer la ligne :

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
avant de fermer immédiatement la socket. Bien sûr, cette ligne n'est pas décodable comme une destination Base 64 valide.

### Flux virtuels SAM : FORWARD

Un client peut utiliser un serveur de sockets classique et attendre des demandes de connexion provenant d'I2P. Pour cela, le client doit :

- ouvrir une nouvelle socket avec le pont SAM
- envoyer la même poignée de main HELLO qu'au-dessus
- envoyer la commande forward

#### Demande de transfert

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Cela permet à la session ${nickname} d'écouter les demandes de connexion entrantes provenant du réseau I2P. FORWARD n'est pas autorisé lorsqu'il y a une commande ACCEPT en attente sur la session.

#### Réponse de transfert

SILENT a comme valeur par défaut false. Que SILENT soit vrai ou faux, le pont SAM répond toujours avec un message STREAM STATUS. Notez qu'il s'agit d'un comportement différent de STREAM ACCEPT et STREAM CONNECT lorsque SILENT=true. Le message STREAM STATUS est :

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
La valeur de RESULTAT peut être l'une des suivantes :

```
OK
I2P_ERROR
INVALID_ID
```
$host est le nom d'hôte ou l'adresse IP du serveur socket auquel SAM transmettra les demandes de connexion. Si non fourni, SAM prend l'adresse IP du socket ayant émis la commande de transfert.

$port est le numéro de port du serveur socket auquel SAM transférera les demandes de connexion. Ce paramètre est obligatoire.

Lorsqu'une demande de connexion arrive depuis I2P, le pont SAM ouvre une connexion socket vers $host:$port. Si celle-ci est acceptée en moins de 3 secondes, SAM acceptera la connexion depuis I2P, puis :

Si SILENT=true est indiqué, toutes les données transitant par la socket actuelle obtenue sont transférées depuis et vers le pair de destination I2P connecté.

Si SILENT=false a été transmis, ce qui correspond à la valeur par défaut, le pont SAM envoie sur la socket obtenue une ligne ASCII contenant la clé publique de destination en base64 du pair demandeur, ainsi que des informations supplémentaires spécifiques à SAM 3.2 uniquement :

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Après cette ligne terminée par '\\n', toutes les données restantes transitant par la socket sont transférées depuis et vers le pair de destination I2P connecté, jusqu'à ce que l'une des deux extrémités ferme la socket.

À partir de SAM 3.2, si SSL=true est spécifié, la socket de transfert utilise SSL/TLS.

Le routeur I2P cessera d'écouter les demandes de connexion entrantes dès que la socket « forwarding » sera fermée.

### Datagrammes SAM

SAMv3 fournit des mécanismes pour envoyer et recevoir des datagrammes via des sockets datagramme locales. Certaines implémentations de SAMv3 prennent également en charge l'ancienne méthode v1/v2 d'envoi et de réception de datagrammes via la socket pont SAM. Les deux méthodes sont documentées ci-dessous.

I2P prend en charge quatre types de datagrammes :

- Les datagrammes réutilisables et authentifiés sont préfixés avec la destination de l'expéditeur et contiennent la signature de l'expéditeur, ce qui permet au destinataire de vérifier que la destination de l'expéditeur n'a pas été falsifiée, et de répondre au datagramme. Le nouveau format Datagram2 est également réutilisable et authentifié.
- Le nouveau format Datagram3 est réutilisable mais non authentifié. Les informations de l'expéditeur ne sont pas vérifiées.
- Les datagrammes bruts ne contiennent ni la destination de l'expéditeur ni de signature.

Les ports I2CP par défaut sont définis pour les datagrammes avec accusé de réception et les datagrammes bruts. Le port I2CP peut être modifié pour les datagrammes bruts.

Un modèle courant de conception de protocole consiste à envoyer des datagrammes répondables vers des serveurs, en incluant un identifiant, et que le serveur réponde par un datagramme brut contenant cet identifiant, afin que la réponse puisse être corrélée avec la requête. Ce modèle élimine le surcoût important lié à l'utilisation de datagrammes répondables dans les réponses. Tous les choix concernant les protocoles et ports I2CP sont spécifiques à l'application, et les concepteurs doivent prendre ces aspects en considération.

Voir également les notes importantes sur l'UTM des datagrammes dans la section ci-dessous.

#### Envoi de datagrammes avec accusé de réception ou bruts

Bien qu'I2P ne contienne pas intrinsèquement d'adresse FROM, une couche supplémentaire est fournie pour faciliter l'utilisation : les datagrammes avec réponse possible (repliable datagrams) — des messages non ordonnés et non fiables pouvant atteindre 31744 octets, incluant une adresse FROM (laissant jusqu'à 1 Ko pour les en-têtes). Cette adresse FROM est authentifiée en interne par SAM (en utilisant la clé de signature de la destination pour vérifier la source) et inclut une protection contre la relecture (replay prevention).

La taille minimale est de 1. Pour une fiabilité optimale de la livraison, la taille maximale recommandée est d'environ 11 Ko. La fiabilité est inversement proportionnelle à la taille du message, peut-être même de façon exponentielle.

Après avoir établi une session SAM avec STYLE=DATAGRAM ou STYLE=RAW, le client peut envoyer des datagrammes avec accusé de réception ou des datagrammes bruts via le port UDP de SAM (7655 par défaut).

La première ligne d'un datagramme envoyé via ce port doit être au format suivant. Tout ceci se trouve sur une seule ligne (séparé par des espaces), affiché sur plusieurs lignes pour plus de clarté :

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 est la version de SAM. À partir de SAM 3.2, toute version 3.x est autorisée.
- $nickname est l'identifiant de la session DATAGRAM qui sera utilisée
- La cible est $destination, qui correspond à la représentation en base 64 de la [Destination](/docs/specs/common-structures#type_Destination), soit 516 caractères base 64 ou plus (387 octets ou plus en binaire), selon le type de signature. **REMARQUE :** Depuis environ 2014 (SAM v3.1), Java I2P prend également en charge les noms d'hôte et les adresses b32 pour $destination, bien que cela n'ait pas été documenté auparavant. Les noms d'hôte et les adresses b32 sont désormais officiellement pris en charge par Java I2P à compter de la version 0.9.48. Le routeur i2pd ne prend actuellement pas en charge les noms d'hôte ni les adresses b32 ; cette fonctionnalité pourrait être ajoutée dans une version ultérieure.
- Toutes les options sont des paramètres par datagramme qui remplacent les valeurs par défaut spécifiées dans la commande SESSION CREATE.
- Les options de version 3.3 SEND_TAGS, TAG_THRESHOLD, EXPIRES et SEND_LEASESET seront transmises à [I2CP](/docs/protocol/i2cp) si elles sont prises en charge. Voir [la spécification I2CP](/docs/protocol/i2cp#msg_SendMessageExpire) pour plus de détails. La prise en charge par le serveur SAM est facultative ; ces options seront ignorées si elles ne sont pas prises en charge.
- cette ligne se termine par '\\n'.

La première ligne sera ignorée par SAM avant l'envoi des données restantes du message à la destination spécifiée.

Pour une méthode alternative d'envoi de datagrammes avec réponse possible et bruts, voir [DATAGRAM SEND et RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagrammes SAM répliquables : réception d'un datagramme

Les datagrammes reçus sont écrits par SAM sur la socket depuis laquelle la session de datagramme a été ouverte, si un PORT de transfert n'est pas spécifié dans la commande SESSION CREATE. C'est la méthode compatible v1/v2 pour recevoir des datagrammes.

Lorsqu'un datagramme arrive, le pont le transmet au client via le message :

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
La source est $destination, qui correspond à la base 64 de la [Destination](/docs/specs/common-structures#type_Destination), soit 516 caractères base 64 ou plus (387 octets ou plus en binaire), selon le type de signature.

Le pont SAM n'expose jamais au client les en-têtes d'authentification ni d'autres champs, uniquement les données fournies par l'expéditeur. Cela se poursuit jusqu'à la fermeture de la session (lorsque le client ferme la connexion).

#### Transmission de datagrammes bruts ou réutilisables

Lors de la création d'une session de datagramme, le client peut demander à SAM de transférer les messages entrants vers une adresse ip:port spécifiée. Pour ce faire, il émet la commande CREATE avec les options PORT et HOST :

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
Le $privkey est le codage en base 64 de la concaténation de la [Destination](/docs/specs/common-structures#type_Destination), suivie de la [Clé privée](/docs/specs/common-structures#type_PrivateKey), suivie de la [Clé privée de signature](/docs/specs/common-structures#type_SigningPrivateKey), éventuellement suivie de la [Signature hors ligne](/docs/specs/common-structures#struct_OfflineSignature), ce qui donne 884 caractères ou plus en base 64 (663 octets ou plus en binaire), selon le type de signature. Le format binaire est spécifié dans le fichier de clé privée.

Les signatures hors ligne sont prises en charge pour les datagrammes RAW, DATAGRAM2 et DATAGRAM3, mais pas pour DATAGRAM. Voir la section SESSION CREATE ci-dessus et la section DATAGRAM2/3 ci-dessous pour plus de détails.

$host est le nom d'hôte ou l'adresse IP du serveur de datagrammes vers lequel SAM transférera les datagrammes. Si non fourni, SAM prend l'adresse IP de la socket ayant émis la commande de transfert.

$port est le numéro de port du serveur de datagrammes vers lequel SAM transférera les datagrammes. Si $port n'est pas défini, les datagrammes NE seront PAS transférés ; ils seront reçus sur la socket de contrôle, de manière compatible avec les versions v1/v2.

Les options supplémentaires fournies sont transmises à la configuration de session I2P si elles ne sont pas interprétées par le pont SAM (par exemple, outbound.length=0). Ces options [sont documentées ci-dessous](#tunnel-i2cp-and-streaming-options).

Les datagrammes transférés avec réponse possible sont toujours préfixés par la destination en base64, sauf pour Datagram3, voir ci-dessous. Lorsqu'un datagramme avec réponse possible arrive, le pont envoie au hôte:port spécifié un paquet UDP contenant les données suivantes :

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
Les datagrammes bruts transférés sont acheminés tels quels vers l'hôte:port spécifié, sans préfixe. Le paquet UDP contient les données suivantes :

```
$datagram_payload
```
À partir de SAM 3.2, lorsque HEADER=true est spécifié dans SESSION CREATE, le datagramme brut transféré sera précédé d'une ligne d'en-tête comme suit :

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Le $destination est la base 64 de la [Destination](/docs/specs/common-structures#type_Destination), qui compte 516 caractères base 64 ou plus (387 octets ou plus en binaire), selon le type de signature.

#### Datagrammes SAM Anonymes (bruts)

En optimisant au maximum la bande passante d'I2P, SAM permet aux clients d'envoyer et de recevoir des datagrammes anonymes, laissant au client lui-même la gestion de l'authentification et des informations de réponse. Ces datagrammes sont non fiables et non ordonnés, et peuvent atteindre jusqu'à 32768 octets.

La taille minimale est de 1. Pour une fiabilité optimale de la livraison, la taille maximale recommandée est d'environ 11 Ko.

Après avoir établi une session SAM avec STYLE=RAW, le client peut envoyer des datagrammes anonymes à travers le pont SAM exactement de la même manière que pour [l'envoi de datagrammes avec réponse possible ou bruts](#sending-repliable-or-raw-datagrams).

Les deux méthodes de réception de datagrammes sont également disponibles pour les datagrammes anonymes.

Les datagrammes reçus sont écrits par SAM sur la socket depuis laquelle la session de datagramme a été ouverte, si un PORT de transfert n'est pas spécifié dans la commande SESSION CREATE. C'est la méthode compatible v1/v2 pour recevoir des datagrammes.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Lorsque des datagrammes anonymes doivent être transférés vers un hôte:port donné, le pont envoie à l'hôte:port spécifié un message contenant les données suivantes :

```
$datagram_payload
```
À partir de SAM 3.2, lorsque HEADER=true est spécifié dans SESSION CREATE, le datagramme brut transféré sera précédé d'une ligne d'en-tête comme suit :

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Pour une méthode alternative d'envoi de datagrammes anonymes, voir [ENVOI BRUT](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagramme 2/3

Les datagrammes 2/3 sont de nouveaux formats spécifiés au début de 2025. Aucune implémentation connue n'existe actuellement. Consultez la documentation de l'implémentation pour connaître l'état actuel. Voir [la spécification](/docs/specs/datagrams) pour plus d'informations.

Il n'existe actuellement aucun projet d'augmenter la version de SAM pour indiquer la prise en charge de Datagram 2/3. Cela pourrait poser problème, car certaines implémentations pourraient souhaiter prendre en charge Datagram 2/3 sans pour autant implémenter les fonctionnalités de SAM v3.3. Toute modification de version reste à déterminer (TBD).

Les Datagram2 et Datagram3 sont tous deux réversibles. Seul le Datagram2 est authentifié.

Datagram2 est identique aux datagrammes avec accusé de réception du point de vue de SAM. Les deux sont authentifiés. Seuls le format I2CP et la signature diffèrent, mais cela n'est pas visible pour les clients SAM. Datagram2 prend également en charge les signatures hors ligne, il peut donc être utilisé par des destinations signées hors ligne.

L'objectif est que Datagram2 remplace les datagrammes avec accusé de réception (Repliable datagrams) pour les nouvelles applications qui n'ont pas besoin de compatibilité ascendante. Datagram2 fournit une protection contre la relecture (replay protection) qui n'est pas disponible pour les datagrammes Repliable. Si la compatibilité ascendante est requise, une application peut prendre en charge à la fois Datagram2 et Repliable sur la même session, avec des sessions PRIMARY SAM 3.3.

Datagram3 est réversible mais non authentifié. Le champ « from » dans le format I2CP est un hachage, pas une destination. La $destination envoyée par le serveur SAM au client sera un hachage base64 de 44 octets. Pour la convertir en une destination complète destinée à une réponse, décodez-la en base64 pour obtenir 32 octets binaires, puis codez ces 32 octets en base32 pour obtenir une chaîne de 52 caractères, et ajoutez ".b32.i2p" afin d'effectuer une RECHERCHE NOMMAGE (NAMING LOOKUP). Comme d'habitude, les clients doivent gérer leur propre cache afin d'éviter des recherches répétées.

Les concepteurs d'applications doivent faire preuve d'une extrême prudence et prendre en compte les implications en matière de sécurité des datagrammes non authentifiés.

#### Considérations sur l'UTM des datagrammes V3

Les datagrammes I2P peuvent être plus gros que le MTU internet typique de 1500 octets. Les datagrammes envoyés localement et les datagrammes transférés avec réponse possible, préfixés par la destination en base64 de 516 octets ou plus, risquent de dépasser ce MTU. Toutefois, les MTU localhost sous Linux sont généralement beaucoup plus élevés, par exemple 65536. Les MTU localhost varient selon le système d'exploitation. Les datagrammes I2P n'excéderont jamais 65536. La taille des datagrammes dépend du protocole d'application.

Si le client SAM est local par rapport au serveur SAM et que le système prend en charge une MTU plus grande, les datagrammes ne seront pas fragmentés localement. Cependant, si le client SAM est distant, les datagrammes IPv4 seront fragmentés et les datagrammes IPv6 échoueront (IPv6 ne prend pas en charge la fragmentation UDP).

Les développeurs de bibliothèques clientes et d'applications devraient être conscients de ces problèmes et documenter des recommandations afin d'éviter la fragmentation et prévenir la perte de paquets, en particulier sur les connexions distantes client-serveur SAM.

#### ENVOI DE DATAGRAMME, ENVOI BRUT (GESTION DES DATAGRAMMES COMPATIBLE V1/V2)

Dans SAM V3, la méthode recommandée pour envoyer des datagrammes est d'utiliser la socket de datagramme sur le port 7655, comme documenté ci-dessus. Toutefois, des datagrammes avec accusé de réception peuvent être envoyés directement via la socket pont SAM en utilisant la commande DATAGRAM SEND, comme décrit dans [SAM V1](/docs/api/sam) et [SAM V2](/docs/api/samv2).

À compter de la version 0.9.14 (version 3.1), les datagrammes anonymes peuvent être envoyés directement via la socket du pont SAM en utilisant la commande RAW SEND, comme documenté dans [SAM V1](/docs/api/sam) et [SAM V2](/docs/api/samv2).

À compter de la version 0.9.24 (version 3.2), DATAGRAM SEND et RAW SEND peuvent inclure les paramètres FROM_PORT=nnnn et/ou TO_PORT=nnnn pour remplacer les ports par défaut. À compter de la version 0.9.24 (version 3.2), RAW SEND peut inclure le paramètre PROTOCOL=nnn pour remplacer le protocole par défaut.

Ces commandes ne prennent *pas* en charge le paramètre ID. Les datagrammes sont envoyés à la session de type DATAGRAM ou RAW créée le plus récemment, selon le cas. La prise en charge du paramètre ID pourrait être ajoutée dans une future version.

Les formats DATAGRAM2 et DATAGRAM3 ne sont *pas* pris en charge de manière compatible avec V1/V2.

### Sessions SAM PRINCIPALES (V3.3 et supérieures)

*La version 3.3 a été introduite dans la version I2P 0.9.25.*

*Dans une version antérieure de cette spécification, les sessions PRIMARY étaient appelées sessions MASTER. Dans `i2pd` et `I2P+`, elles sont toujours appelées uniquement sessions MASTER.*

SAM v3.3 ajoute la prise en charge de l'exécution de flux, de datagrammes et de sous-sessions brutes sur la même session principale, ainsi que la possibilité d'exécuter plusieurs sous-sessions du même type. Tout le trafic des sous-sessions utilise une destination unique, ou un ensemble de tunnels unique. Le routage du trafic vers I2P est basé sur les options de port et de protocole des sous-sessions.

Pour créer des sous-sessions multiplexées, vous devez d'abord créer une session principale, puis ajouter des sous-sessions à cette session principale. Chaque sous-session doit posséder un identifiant unique ainsi qu'un protocole et un port d'écoute uniques. Les sous-sessions peuvent également être supprimées de la session principale.

Avec une session PRINCIPALE et une combinaison de sous-sessions, un client SAM peut prendre en charge plusieurs applications, ou une seule application sophistiquée utilisant divers protocoles, sur un même ensemble de tunnels. Par exemple, un client BitTorrent pourrait configurer une sous-session de streaming pour les connexions pair-à-pair, ainsi que des sous-sessions datagramme et brute pour les communications DHT.

#### Création d'une session PRINCIPALE

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Le pont SAM répondra par un succès ou un échec, comme indiqué dans [la réponse à une création de session standard](#session-creation-response).

Ne définissez pas les options PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL ou HEADER sur une session principale. Vous ne pouvez envoyer aucune donnée sur un identifiant de session PRIMARY ni sur la socket de contrôle. Toutes les commandes telles que STREAM CONNECT, DATAGRAM SEND, etc., doivent utiliser l'identifiant de sous-session sur une socket séparée.

La session PRINCIPALE se connecte au routeur et crée des tunnels. Lorsque le pont SAM répond, les tunnels ont été créés et la session est prête à accueillir des sous-sessions. Toutes les options [I2CP](/docs/protocol/i2cp) relatives aux paramètres des tunnels, tels que la longueur, la quantité et le surnom, doivent être fournies lors de la création de la session principale (SESSION CREATE).

Toutes les commandes utilitaires sont prises en charge sur une session principale.

Lorsque la session principale est fermée, toutes les sous-sessions sont également fermées.

REMARQUE : Avant la version 0.9.47, utilisez STYLE=MASTER. STYLE=PRIMARY est pris en charge à partir de la version 0.9.47. MASTER est toujours pris en charge pour des raisons de compatibilité ascendante.

#### Création d'une sous-session

En utilisant le même socket de contrôle sur lequel la session PRINCIPALE a été créée :

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Le pont SAM répondra par un succès ou un échec, comme indiqué dans [la réponse à une création de SESSION standard](#session-creation-response). Étant donné que les tunnels ont déjà été créés lors de la création de SESSION principale, le pont SAM devrait répondre immédiatement.

Ne définissez pas l'option DESTINATION lors d'un SESSION ADD. La sous-session utilisera la destination spécifiée dans la session principale. Toutes les sous-sessions doivent être ajoutées sur la socket de contrôle, c'est-à-dire la même connexion que celle sur laquelle vous avez créé la session principale.

Les multiples sous-sessions doivent avoir des options suffisamment uniques pour que les données entrantes puissent être acheminées correctement. En particulier, plusieurs sessions du même style doivent avoir des options LISTEN_PORT différentes (et/ou LISTEN_PROTOCOL, uniquement pour RAW). Une commande SESSION ADD avec un port d'écoute et un protocole dupliquant une sous-session existante entraînera une erreur.

Le LISTEN_PORT est le port I2P local, c'est-à-dire le port de réception (TO) pour les données entrantes. Si le LISTEN_PORT n'est pas spécifié, la valeur de FROM_PORT sera utilisée. Si ni LISTEN_PORT ni FROM_PORT ne sont spécifiés, le routage entrant sera basé uniquement sur STYLE et PROTOCOL. Pour LISTEN_PORT et LISTEN_PROTOCOL, la valeur 0 signifie « n'importe quelle valeur », c'est-à-dire un caractère générique (wildcard). Si LISTEN_PORT et LISTEN_PROTOCOL sont tous deux à 0, cette sous-session sera celle par défaut pour le trafic entrant qui n'est pas acheminé vers une autre sous-session. Le trafic entrant en streaming (protocole 6) ne sera jamais acheminé vers une sous-session RAW, même si son LISTEN_PROTOCOL est 0. Une sous-session RAW ne peut pas définir un LISTEN_PROTOCOL égal à 6. S'il n'existe ni sous-session par défaut ni sous-session correspondant au protocole et au port du trafic entrant, ces données seront rejetées.

Utilisez l'ID de sous-session, et non l'ID de session principal, pour envoyer et recevoir des données. Toutes les commandes telles que STREAM CONNECT, DATAGRAM SEND, etc., doivent utiliser l'ID de sous-session.

Toutes les commandes utilitaires sont prises en charge sur une session principale ou une sous-session. L'envoi/réception de datagrammes/bruts en v1/v2 n'est pas pris en charge sur une session principale ou sur des sous-sessions.

#### Arrêter une sous-session

En utilisant le même socket de contrôle sur lequel la session PRINCIPALE a été créée :

```
->  SESSION REMOVE
          ID=$nickname
```
Ceci supprime une sous-session de la session principale. Ne définissez aucune autre option lors d'une commande SESSION REMOVE. Les sous-sessions doivent être supprimées via la socket de contrôle, c'est-à-dire la même connexion sur laquelle vous avez créé la session principale. Une fois qu'une sous-session est supprimée, elle est fermée et ne peut plus être utilisée pour envoyer ou recevoir des données.

Le pont SAM répondra par un succès ou un échec, comme indiqué dans [la réponse à une création de session standard](#session-creation-response).

### Commandes utilitaires SAM

Certaines commandes utilitaires nécessitent une session préexistante et d'autres non. Voir les détails ci-dessous.

#### Recherche de nom d'hôte

Le message suivant peut être utilisé par le client pour interroger le pont SAM afin de résoudre un nom :

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
auquel on répond par

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
La valeur de RESULTAT peut être l'une des suivantes :

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Si NAME=ME, la réponse contiendra la destination utilisée par la session en cours (utile si vous utilisez une destination TRANSIENT). Si $result n'est pas OK, MESSAGE peut transmettre un message descriptif, tel que « mauvais format », etc. INVALID_KEY implique qu'il y a un problème avec $name dans la requête, possiblement des caractères invalides.

Le $destination est la base 64 de la [Destination](/docs/specs/common-structures#type_Destination), qui compte 516 caractères base 64 ou plus (387 octets ou plus en binaire), selon le type de signature.

NAMING LOOKUP ne nécessite pas qu'une session ait été créée au préalable. Cependant, dans certaines implémentations, une recherche .b32.i2p non mise en cache et nécessitant une requête réseau peut échouer, car aucun tunnel client n'est disponible pour la recherche.

#### Options de recherche de nom

NAMING LOOKUP est étendu depuis l'API du routeur 0.9.66 pour prendre en charge les recherches de services. La prise en charge peut varier selon les implémentations. Voir la proposition 167 pour plus d'informations.

NAMING LOOKUP NAME=example.i2p OPTIONS=true demande la correspondance des options dans la réponse. NAME peut être une destination base64 complète lorsque OPTIONS=true.

Si la recherche de destination a réussi et que des options étaient présentes dans le leaseset, alors dans la réponse, après la destination, apparaîtront une ou plusieurs options sous la forme OPTION:clé=valeur. Chaque option aura son propre préfixe OPTION:. Toutes les options du leaseset seront incluses, et pas seulement les options d'enregistrement de service. Par exemple, des options pour des paramètres définis à l'avenir pourraient être présentes. Exemple :

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Les clés contenant '=', ainsi que les clés ou valeurs contenant un saut de ligne, sont considérées comme invalides et la paire clé/valeur sera supprimée de la réponse. S'il n'y a aucune option présente dans le leaseset, ou si le leaseset est en version 1, la réponse n'inclura aucune option. Si OPTIONS=true était inclus dans la requête et que le leaseset n'est pas trouvé, une nouvelle valeur de résultat LEASESET_NOT_FOUND sera retournée.

#### Génération de la clé de destination

Les clés base64 publiques et privées peuvent être générées à l'aide du message suivant :

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
auquel on répond par

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Depuis la version 3.1 (I2P 0.9.14), un paramètre optionnel SIGNATURE_TYPE est pris en charge. La valeur de SIGNATURE_TYPE peut être n'importe quel nom (par exemple ECDSA_SHA256_P256, insensible à la casse) ou nombre (par exemple 1) pris en charge par les [certificats de clé](/docs/specs/common-structures#type_Certificate). La valeur par défaut est DSA_SHA1, ce qui n'est PAS ce que vous souhaitez. Pour la plupart des applications, veuillez spécifier SIGNATURE_TYPE=7.

Le $destination est la base 64 de la [Destination](/docs/specs/common-structures#type_Destination), qui compte 516 caractères base 64 ou plus (387 octets ou plus en binaire), selon le type de signature.

Le $privkey est la représentation en base 64 de la concaténation de la [Destination](/docs/specs/common-structures#type_Destination), suivie de la [Clé Privée](/docs/specs/common-structures#type_PrivateKey), suivie de la [Clé Privée de Signature](/docs/specs/common-structures#type_SigningPrivateKey), ce qui donne 884 caractères base 64 ou plus (663 octets ou plus en binaire), selon le type de signature. Le format binaire est spécifié dans le fichier de clé privée.

Remarques concernant la clé privée binaire de 256 octets [Private Key](/docs/specs/common-structures#type_PrivateKey) : ce champ n'est plus utilisé depuis la version 0.6 (2005). Les implémentations SAM peuvent envoyer des données aléatoires ou uniquement des zéros dans ce champ ; ne soyez pas surpris par une chaîne de AAAA en base 64. La plupart des applications stockent simplement la chaîne en base 64 et la renvoient telle quelle lors de la SESSION CREATE, ou la décodent en binaire pour le stockage, puis la recodent pour la SESSION CREATE. Toutefois, les applications peuvent choisir de décoder la base 64, analyser les données binaires conformément à la spécification PrivateKeyFile, supprimer la partie correspondant à la clé privée de 256 octets, puis la remplacer par 256 octets de données aléatoires ou uniquement des zéros lors du recodage pour la SESSION CREATE. TOUTES les autres données de la spécification PrivateKeyFile doivent être conservées. Cela permettrait d’économiser 256 octets de stockage sur le système de fichiers, mais cela n’en vaut probablement pas la peine pour la plupart des applications. Voir la proposition 161 pour plus d’informations et de contexte.

DEST GENERATE ne nécessite pas qu'une session ait été créée au préalable.

DEST GENERATE ne peut pas être utilisé pour créer une destination avec des signatures hors ligne.

#### PING/PONG (SAM 3.2 ou supérieur)

Le client ou le serveur peut envoyer :

```
PING[ arbitrary text]
```
sur le port de contrôle, avec la réponse :

```
PONG[ arbitrary text from the ping]
```
à utiliser pour la conservation de la connexion du socket de contrôle. Chaque côté peut fermer la session et le socket si aucune réponse n'est reçue dans un délai raisonnable, selon l'implémentation.

Si un délai d'attente se produit en attendant un PONG du client, le pont peut envoyer :

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
puis se déconnecter.

Si un délai d'attente se produit en attendant un PONG depuis le pont, le client peut simplement se déconnecter.

PING/PONG ne nécessite pas qu'une session ait été créée au préalable.

#### QUIT/STOP/EXIT (SAM 3.2 ou supérieur, fonctionnalités facultatives)

Les commandes QUIT, STOP et EXIT fermeront la session et la socket. La mise en œuvre est facultative, pour faciliter les tests via telnet. La question de savoir s'il y a une réponse avant la fermeture de la socket (par exemple, un message SESSION STATUS) dépend de l'implémentation et n'entre pas dans le cadre de cette spécification.

QUIT/STOP/EXIT ne nécessitent pas qu'une session ait été créée au préalable.

#### AIDE (fonctionnalité facultative)

Les serveurs peuvent implémenter une commande HELP. Cette implémentation est facultative, afin de faciliter les tests via telnet. Le format de sortie et la détection de la fin de la sortie dépendent de l'implémentation et ne relèvent pas du présent document de spécification.

HELP ne nécessite pas qu'une session ait été créée au préalable.

#### Configuration de l'autorisation (SAM 3.2 ou supérieur, fonctionnalité facultative)

Configuration de l'autorisation utilisant la commande AUTH. Un serveur SAM peut implémenter ces commandes afin de faciliter le stockage persistant des identifiants. La configuration de l'authentification autrement que par ces commandes dépend de l'implémentation et n'entre pas dans le cadre de cette spécification.

- AUTH ENABLE active l'autorisation sur les connexions ultérieures
- AUTH DISABLE désactive l'autorisation sur les connexions ultérieures
- AUTH ADD USER="foo" PASSWORD="bar" ajoute un utilisateur/mot de passe
- AUTH REMOVE USER="foo" supprime cet utilisateur

Les guillemets doubles pour l'utilisateur et le mot de passe sont recommandés mais pas obligatoires. Un guillemet double à l'intérieur d'un nom d'utilisateur ou d'un mot de passe doit être échappé avec une barre oblique inverse. En cas d'échec, le serveur répondra avec un I2P_ERROR et un message.

AUTH ne nécessite pas qu'une session ait été créée au préalable.

### Valeurs RESULT

Voici les valeurs que peut contenir le champ RESULT, accompagnées de leur signification :

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Les différentes implémentations peuvent ne pas être cohérentes quant au RESULTAT renvoyé dans divers scénarios.

La plupart des réponses accompagnées d'un RESULTAT, autre que OK, incluront également un MESSAGE contenant des informations supplémentaires. Le MESSAGE sera généralement utile pour le débogage. Toutefois, les chaînes MESSAGE dépendent de l'implémentation, peuvent ou non être traduites par le serveur SAM selon les paramètres régionaux actuels, peuvent contenir des informations internes spécifiques à l'implémentation telles que des exceptions, et sont susceptibles d'être modifiées sans préavis. Bien que les clients SAM puissent choisir d'exposer les chaînes MESSAGE aux utilisateurs, ils ne doivent pas prendre de décisions programmatiques basées sur ces chaînes, car cela rendrait leur fonctionnement fragile.

### Options de tunnel, I2CP et de streaming

Ces options peuvent être transmises sous forme de paires nom=valeur dans la ligne SAM SESSION CREATE.

Toutes les sessions peuvent inclure des [options I2CP telles que les longueurs et quantités de tunnels](/docs/protocol/i2cp#options). Les sessions STREAM peuvent inclure des [options de la bibliothèque de streaming](/docs/api/streaming#options).

Voir ces références pour les noms d'options et les valeurs par défaut. La documentation référencée concerne l'implémentation du routeur Java. Les valeurs par défaut sont susceptibles d'être modifiées. Les noms et valeurs d'options sont sensibles à la casse. D'autres implémentations de routeurs peuvent ne pas prendre en charge toutes les options et peuvent avoir des valeurs par défaut différentes ; consultez la documentation de votre routeur pour plus de détails.

### Notes sur le codage Base64

Le codage Base 64 doit utiliser l'alphabet Base 64 standard I2P « A-Z, a-z, 0-9, -, ~ ».

### Configuration SAM par défaut

Le port SAM par défaut est 7656. SAM n'est pas activé par défaut dans le routeur Java I2P ; il doit être démarré manuellement, ou configuré pour démarrer automatiquement, sur la page de configuration des clients dans la console du routeur, ou dans le fichier clients.config. Le port UDP SAM par défaut est 7655, en écoute sur 127.0.0.1. Ces valeurs peuvent être modifiées dans le routeur Java en ajoutant les arguments sam.udp.port=nnnnn et/ou sam.udp.host=w.x.y.z à l'appel, ou sur la ligne SESSION.

La configuration dans d'autres routeurs dépend de l'implémentation. Voir [le guide de configuration d'i2pd ici](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
