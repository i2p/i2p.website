---
title: "Spécification de mise à jour logicielle"
description: "Mécanisme de mise à jour signé et sécurisé et structure du flux pour les routers I2P"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Vue d'ensemble

Routers vérifient automatiquement la disponibilité de mises à jour en interrogeant un flux d’actualités signé, distribué via le réseau I2P. Lorsqu’une version plus récente est annoncée, le router télécharge une archive de mise à jour signée cryptographiquement (`.su3`) et la prépare pour l’installation. Ce système garantit une distribution des versions officielles **authentifiée, résistante aux altérations** et **multicanale**.

À partir d’I2P 2.10.0, le système de mise à jour utilise: - **RSA-4096 / SHA-512** signatures - **Format de conteneur SU3** (remplaçant les anciens SUD/SU2) - **Miroirs redondants:** HTTP dans le réseau I2P, HTTPS en clearnet (Internet public), et BitTorrent

---

## 1. Fil d'actualité

Les routers interrogent périodiquement le flux Atom signé à intervalles de quelques heures afin de découvrir de nouvelles versions et des avis de sécurité. Le flux est signé et distribué sous la forme d’un fichier `.su3`, qui peut inclure :

- `<i2p:version>` — nouveau numéro de version  
- `<i2p:minVersion>` — version minimale prise en charge du router  
- `<i2p:minJavaVersion>` — environnement d'exécution Java minimal requis  
- `<i2p:update>` — énumère plusieurs miroirs de téléchargement (I2P, HTTPS, torrent)  
- `<i2p:revocations>` — données de révocation de certificats  
- `<i2p:blocklist>` — listes de blocage au niveau du réseau pour les pairs compromis

### Distribution du flux

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Les routers privilégient le flux I2P, mais peuvent basculer vers le clearnet (Internet public) ou une distribution par torrent si nécessaire.

---

## 2. Formats de fichiers

### SU3 (Norme actuelle)

Introduit en 0.9.9, SU3 a remplacé les anciens formats SUD et SU2. Chaque fichier contient un en-tête, une charge utile et une signature en fin de fichier.

**Structure de l'en-tête** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**Étapes de vérification de la signature** 1. Analyser l'en-tête et identifier l'algorithme de signature.   2. Vérifier le hachage et la signature à l'aide du certificat du signataire stocké.   3. Confirmer que le signataire n'est pas révoqué.   4. Comparer la chaîne de version intégrée avec les métadonnées de la charge utile.

Les routers sont livrés avec des certificats de signataire de confiance (actuellement **zzz** et **str4d**) et rejettent toutes les sources non signées ou révoquées.

### SU2 (Obsolète)

- Utilisait l'extension `.su2` avec des fichiers JAR compressés avec Pack200 (format de compression Java).  
- Supprimé après que Java 14 a déprécié Pack200 (JEP 367).  
- Désactivé dans I2P 0.9.48+; désormais entièrement remplacé par la compression ZIP.

### SUD (ancien)

- Ancien format ZIP signé DSA-SHA1 (avant 0.9.9).  
- Aucun identifiant de signataire ni en-tête, intégrité limitée.  
- Remplacé en raison d'une cryptographie faible et de l'absence de contrainte de version.

---

## 3. Flux de mise à jour

### 3.1 Vérification de l’en-tête

Routers ne récupèrent que l’**en-tête SU3** pour vérifier la chaîne de version avant de télécharger les fichiers complets.   Cela évite de gaspiller de la bande passante sur des miroirs périmés ou des versions obsolètes.

### 3.2 Téléchargement complet

Après vérification de l’en-tête, le router télécharge le fichier `.su3` complet depuis: - Miroirs eepsite intra-réseau (préféré)   - Miroirs HTTPS clearnet (solution de repli)   - BitTorrent (distribution facultative assistée par les pairs)

Les téléchargements utilisent des clients HTTP I2PTunnel standard, avec réessais, gestion des délais d'expiration et repli sur un miroir.

### 3.3 Vérification de la signature

Chaque fichier téléchargé est soumis à: - **Contrôle de la signature:** Vérification RSA-4096/SHA512   - **Correspondance de version:** Vérification de la version de l'en-tête par rapport à celle de la charge utile   - **Prévention de la rétrogradation:** Garantit que la mise à jour est plus récente que la version installée

Les fichiers invalides ou non correspondants sont immédiatement rejetés.

### 3.4 Préparation de l'installation

Après vérification: 1. Extraire le contenu du ZIP dans un répertoire temporaire   2. Supprimer les fichiers répertoriés dans `deletelist.txt`   3. Remplacer les bibliothèques natives si `lib/jbigi.jar` est présent   4. Copier les certificats des signataires dans `~/.i2p/certificates/`   5. Renommer la mise à jour en `i2pupdate.zip` afin qu'elle soit appliquée au prochain redémarrage

La mise à jour s’installe automatiquement au prochain démarrage ou lorsque vous déclenchez manuellement « Installer la mise à jour maintenant ».

---

## 4. Gestion des fichiers

### deletelist.txt

Une liste en texte brut des fichiers obsolètes à supprimer avant d’extraire les nouveaux contenus.

**Règles:** - Un chemin par ligne (chemins relatifs uniquement) - Lignes commençant par `#` ignorées - `..` et chemins absolus rejetés

### Bibliothèques natives

Pour éviter des binaires natifs périmés ou incompatibles : - Si `lib/jbigi.jar` existe, les anciens fichiers `.so` ou `.dll` sont supprimés   - Assure que les bibliothèques spécifiques à la plateforme sont fraîchement extraites

---

## 5. Gestion des certificats

Routers peuvent recevoir **de nouveaux certificats de signature** au moyen de mises à jour ou de révocations transmises par le flux d’actualités.

- Les nouveaux fichiers `.crt` sont copiés dans le répertoire des certificats.  
- Les certificats révoqués sont supprimés avant les vérifications ultérieures.  
- Prend en charge la rotation des clés sans nécessiter d'intervention manuelle de l'utilisateur.

Toutes les mises à jour sont signées hors ligne à l'aide de **air-gapped signing systems (systèmes de signature isolés du réseau)**.   Les clés privées ne sont jamais stockées sur les serveurs de build.

---

## 6. Directives pour les développeurs

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
Les prochaines versions exploreront l’intégration de signatures post-quantiques (voir la proposition 169) et des compilations reproductibles.

---

## 7. Vue d'ensemble de la sécurité

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Versionnage

- Router: **2.10.0 (API 0.9.67)**  
- Versionnage sémantique avec `Major.Minor.Patch`.  
- L'application d'une version minimale empêche les mises à niveau dangereuses.  
- Java pris en charge : **Java 8–17**. À partir de 2.11.0+, Java 17+ sera requis.

---
