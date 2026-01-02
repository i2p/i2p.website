---
title: "Base de données du réseau"
description: "Comprendre la base de données réseau distribuée d'I2P (netDb) - une table de hachage distribuée spécialisée pour les informations de contact du router et les recherches de destinations"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Aperçu

Le **netDb** est une base de données distribuée spécialisée ne contenant que deux types de données : - **RouterInfos** – informations de contact du router - **LeaseSets** – informations de contact de la destination

Toutes les données sont signées cryptographiquement et vérifiables. Chaque entrée inclut des informations de liveness (indicateurs d'activité) permettant d’éliminer les entrées obsolètes et de remplacer celles périmées, ce qui protège contre certaines classes d’attaques.

La distribution utilise un mécanisme de **floodfill** (propagation en inondation), où un sous-ensemble de routers maintient la base de données distribuée.

---

## 2. RouterInfo

Lorsque des routers ont besoin de contacter d'autres routers, ils échangent des paquets **RouterInfo** contenant :

- **Identité du router** – clé de chiffrement, clé de signature, certificat
- **Adresses de contact** – comment joindre le router
- **Horodatage de publication** – quand ces informations ont été publiées
- **Options textuelles arbitraires** – indicateurs de capacité et paramètres
- **Signature cryptographique** – prouve l'authenticité

### 2.1 Drapeaux de capacités

Les routers annoncent leurs capacités via des codes alphabétiques dans leur RouterInfo (informations du router):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Classes de bande passante

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Valeurs d'ID de réseau

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 Statistiques de RouterInfo

Les Routers publient des statistiques de santé facultatives pour l'analyse du réseau: - Taux de réussite/rejet/dépassement de délai de la construction des tunnels exploratoires - Nombre moyen sur 1 heure de tunnels participants

Les statistiques suivent le format `stat_(statname).(statperiod)` avec des valeurs séparées par des points-virgules.

**Exemple de statistiques:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Les Floodfill routers peuvent également publier : `netdb.knownLeaseSets` et `netdb.knownRouters`

### 2.5 Options de la famille

À partir de la version 0.9.24, les routers peuvent déclarer leur appartenance à une famille (même opérateur):

- **family**: Nom de la famille
- **family.key**: Code du type de signature concaténé avec la clé publique de signature encodée en base64
- **family.sig**: Signature du nom de la famille et du hachage de 32 octets du router

Plusieurs routers appartenant à la même famille ne seront pas utilisés dans un même tunnel.

### 2.6 Expiration de RouterInfo

- Pas d'expiration pendant la première heure de fonctionnement
- Pas d'expiration avec 25 RouterInfos stockés ou moins
- La durée d'expiration diminue à mesure que le nombre local augmente (72 heures pour <120 routers ; ~30 heures pour 300 routers)
- Les SSU introducers expirent en ~1 heure
- Les Floodfills (nœuds floodfill d'I2P) utilisent une expiration d'une heure pour tous les RouterInfos locaux

---

## 3. LeaseSet

**LeaseSets** décrivent les points d'entrée de tunnel pour des destinations particulières et précisent :

- **Identité du router passerelle du tunnel**
- **ID de tunnel sur 4 octets**
- **Heure d’expiration du tunnel**

Les LeaseSets comprennent : - **Destination** – clé de chiffrement, clé de signature, certificat - **Clé publique de chiffrement supplémentaire** – pour la garlic encryption (technique de chiffrement « garlic » propre à I2P) de bout en bout - **Clé publique de signature supplémentaire** – destinée à la révocation (actuellement inutilisée) - **Signature cryptographique**

### 3.1 Variantes de LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 Expiration du LeaseSet (ensemble de baux)

Les LeaseSets (structures publiant les baux de tunnels entrants) standard expirent à l’expiration la plus tardive de leurs baux. L’expiration d’un LeaseSet2 est spécifiée dans l’en-tête. Les expirations des EncryptedLeaseSet et MetaLeaseSet peuvent varier, avec, le cas échéant, l’application d’une durée maximale.

---

## 4. Amorçage

La netDb décentralisée nécessite au moins une référence à un pair pour s’intégrer. Le **réensemencement** récupère des fichiers RouterInfo (métadonnées d’un router I2P) (`routerInfo-$hash.dat`) depuis les répertoires netDb de volontaires. Au premier démarrage, le téléchargement depuis des URL codées en dur sélectionnées aléatoirement est effectué automatiquement.

---

## 5. Mécanisme de Floodfill

Le netDb floodfill utilise un stockage distribué simple : il suffit d’envoyer les données au pair floodfill le plus proche. Lorsque des pairs non-floodfill envoient des éléments à stocker, les floodfills les transmettent à un sous-ensemble de pairs floodfill les plus proches de la clé donnée.

La participation au floodfill est signalée par un indicateur de capacité (`f`) dans RouterInfo.

### 5.1 Exigences pour la participation volontaire à Floodfill

Contrairement aux serveurs d'annuaire de confiance codés en dur de Tor, l'ensemble floodfill d'I2P est **non approuvé** et évolue au fil du temps.

Floodfill s’active automatiquement uniquement sur les routers à haut débit qui répondent à ces exigences: - Bande passante partagée minimale de 128 KBytes/sec (configurée manuellement) - Doit réussir des tests de santé supplémentaires (temps de file d’attente des messages sortants, retard des tâches)

L’activation automatique actuelle se traduit par environ **6 % de participation au floodfill du réseau**.

Des floodfills (nœuds spéciaux qui stockent et propagent la netDb) configurés manuellement coexistent avec des volontaires automatiques. Lorsque le nombre de floodfills passe en dessous du seuil, les routers à bande passante élevée se portent automatiquement volontaires. Quand il y a trop de floodfills, ils cessent de faire office de floodfill.

### 5.2 Rôles de floodfill

Outre l’acceptation des opérations de stockage netDb et la réponse aux requêtes, les floodfills assurent des fonctions standard de router. Leur bande passante plus élevée se traduit généralement par une participation accrue aux tunnel, mais cela n’est pas directement lié aux services de base de données.

---

## 6. Métrique de proximité de Kademlia

Le netDb utilise une mesure de distance **de style Kademlia** basée sur XOR. Le hachage SHA256 de RouterIdentity ou Destination crée la clé Kademlia (sauf pour les LS2 Encrypted LeaseSets, qui utilisent SHA256 de l'octet de type 3 plus la clé publique aveuglée).

### 6.1 Rotation de l'espace de clés

Pour augmenter le coût d'une attaque Sybil, au lieu d'utiliser `SHA256(key)`, le système utilise :

```
SHA256(key + yyyyMMdd)
```
où la date est une date UTC en ASCII sur 8 octets. Cela crée la **clé de routage**, qui change quotidiennement à minuit UTC — appelé **rotation de l'espace de clés**.

Les clés de routage ne sont jamais transmises dans les messages I2NP ; elles sont utilisées uniquement pour la détermination locale de la distance.

---

## 7. Segmentation de la base de données réseau

Les DHT Kademlia traditionnelles ne préservent pas la non-corrélabilité des informations stockées. I2P empêche les attaques visant à associer des tunnels clients aux routers en implémentant la **segmentation**.

### 7.1 Stratégie de segmentation

Les Routers suivent : - Si les entrées sont arrivées via des tunnels clients ou directement - Si via un tunnel, quel tunnel client/destination - Les arrivées via plusieurs tunnels sont suivies - Les réponses de stockage sont distinguées des réponses de recherche

Les implémentations Java et C++ utilisent toutes deux : - Une **"Principale" netDb** pour les recherches directes/opérations de floodfill dans le contexte du router - **"Bases de données réseau client"** ou **"Sous-bases de données"** dans des contextes client, capturant les entrées envoyées aux tunnels client

Les netDbs clients n'existent que pendant la durée de vie du client et ne contiennent que des entrées de tunnels clients. Les entrées provenant des tunnels clients ne peuvent pas chevaucher les arrivées directes.

Chaque netDb enregistre si les entrées sont arrivées sous forme de stores (messages de stockage; répondent aux requêtes de recherche) ou sous forme de réponses de recherche (ne répondent que si elles ont été préalablement stockées pour la même destination). Les clients ne répondent jamais aux requêtes avec des entrées du Main netDb, uniquement avec des entrées de la base de données réseau client.

Les stratégies combinées **segmentent** le netDb pour contrer les attaques d'association client-router.

---

## 8. Stockage, vérification et recherche

### 8.1 Stockage de RouterInfo (métadonnées du router) auprès des pairs

I2NP `DatabaseStoreMessage` contenant l’échange de RouterInfo local lors de l’initialisation de la connexion de transport NTCP ou SSU.

### 8.2 Stockage du LeaseSet chez les pairs

Les I2NP `DatabaseStoreMessage` contenant le LeaseSet local sont échangés périodiquement via des messages chiffrés avec garlic encryption (technique de chiffrement « garlic » propre à I2P), regroupés avec le trafic de la Destination (identité d’adresse publique I2P), ce qui permet des réponses sans recherche du LeaseSet.

### 8.3 Sélection des floodfill

`DatabaseStoreMessage` envoie au floodfill le plus proche de la clé de routage actuelle. Le floodfill le plus proche est trouvé via une recherche dans la base de données locale. Même s’il n’est pas réellement le plus proche, la diffusion le propage "plus près" en l’envoyant à plusieurs floodfills.

Kademlia traditionnel utilise une recherche "find-closest" (recherche du nœud le plus proche) avant l'insertion. Bien que I2NP ne dispose pas de tels messages, les routers peuvent effectuer une recherche itérative en inversant le bit de poids faible (`key ^ 0x01`) afin de garantir la découverte du pair réellement le plus proche.

### 8.4 Stockage des RouterInfo dans les floodfills

Les routers publient leur RouterInfo en se connectant directement à un floodfill, en envoyant un message I2NP `DatabaseStoreMessage` avec un Reply Token (jeton de réponse) non nul. Le message n’est pas chiffré de bout en bout via garlic encryption (connexion directe, sans intermédiaires). Le floodfill répond avec `DeliveryStatusMessage` en utilisant le Reply Token comme identifiant de message.

Les Routers peuvent également envoyer leur RouterInfo (informations du router) via un tunnel exploratoire (limites de connexion, incompatibilité, masquage d’IP). Les Floodfills peuvent rejeter de telles opérations de stockage en cas de surcharge.

### 8.5 Publication du LeaseSet aux Floodfills

Le stockage des LeaseSet est plus sensible que celui des RouterInfo. Les Routers doivent empêcher toute association de LeaseSet avec eux-mêmes.

Les routers publient un LeaseSet via un tunnel client sortant au moyen d’un `DatabaseStoreMessage` avec un jeton de réponse non nul. Le message est chiffré de bout en bout au moyen de garlic encryption en utilisant le gestionnaire de clés de session de la Destination, ce qui le dissimule à l’extrémité sortante du tunnel. Floodfill répond avec un `DeliveryStatusMessage` renvoyé via un tunnel entrant.

### 8.6 Processus d'inondation

Les Floodfills valident les RouterInfo (informations du router)/LeaseSet avant de les stocker localement, en utilisant des critères adaptatifs dépendant de la charge, de la taille du netdb et d'autres facteurs.

Après réception de nouvelles données valides, les floodfills les "inondent" en recherchant les 3 floodfill routers les plus proches de la clé de routage. Les connexions directes envoient un I2NP `DatabaseStoreMessage` avec un jeton de réponse égal à zéro. Les autres routers ne répondent pas et ne ré-inondent pas.

**Contraintes importantes:** - Les Floodfills ne doivent pas propager via des tunnels; uniquement des connexions directes - Les Floodfills ne propagent jamais un LeaseSet expiré ni un RouterInfo publié il y a plus d'une heure

### 8.7 Recherche de RouterInfo (informations du router) et de LeaseSet

I2NP `DatabaseLookupMessage` demande des entrées netdb aux routers floodfill. Les recherches sont envoyées via un tunnel d'exploration sortant ; les réponses spécifient le tunnel d'exploration entrant pour le retour.

Les recherches envoient généralement vers deux routeurs floodfill "fiables" les plus proches de la clé demandée, en parallèle.

- **Correspondance locale**: reçoit une réponse I2NP `DatabaseStoreMessage`
- **Aucune correspondance locale**: reçoit un I2NP `DatabaseSearchReplyMessage` avec des références à d'autres floodfill router (nœuds spécialisés qui stockent et propagent le netDb) proches de la clé

Les recherches de LeaseSet utilisent la garlic encryption (chiffrement "garlic", agrégation de messages propre à I2P) de bout en bout (depuis la version 0.9.5). Les recherches de RouterInfo (métadonnées d'un router I2P) ne sont pas chiffrées en raison du coût de calcul d'ElGamal, ce qui les rend vulnérables à l'espionnage au niveau de l'extrémité sortante.

À partir de la version 0.9.7, les réponses de recherche incluent la clé de session et un tag de session, masquant ces réponses à la passerelle d'entrée.

### 8.8 Recherches itératives

Avant la version 0.8.9 : Deux recherches redondantes en parallèle sans routage récursif ni itératif.

À partir de la version 0.8.9: **Recherches itératives** mises en œuvre sans redondance—plus efficaces, fiables et adaptées à une connaissance incomplète des floodfills. À mesure que le réseau croît et que les routers connaissent moins de floodfills, les recherches approchent une complexité O(log n).

Les recherches itératives se poursuivent même sans références vers des pairs plus proches, afin d’empêcher le black-holing malveillant (mise en trou noir du trafic). Les limites actuelles de nombre maximal de requêtes et de délai d’expiration s’appliquent.

### 8.9 Vérification

**RouterInfo Verification**: Désactivée à partir de la version 0.9.7.1 afin d'empêcher les attaques décrites dans l'article "Practical Attacks Against the I2P Network".

**Vérification du LeaseSet**: Les routers attendent ~10 secondes, puis effectuent une recherche depuis un floodfill différent via un tunnel client sortant. Le garlic encryption de bout en bout masque cela à l’extrémité sortante. Les réponses reviennent via des tunnels entrants.

À partir de la version 0.9.7, les réponses sont chiffrées en masquant la clé de session et le tag (étiquette) à la passerelle entrante.

### 8.10 Exploration

**Exploration** implique une recherche netdb (base de données réseau) avec des clés aléatoires pour découvrir de nouveaux routers. Les Floodfills (nœuds floodfill spéciaux) répondent avec `DatabaseSearchReplyMessage` contenant des hachages de routers non-floodfill proches de la clé demandée. Les requêtes d’exploration définissent un indicateur spécial dans `DatabaseLookupMessage`.

---

## 9. MultiHoming (rattachement à plusieurs réseaux)

Les Destinations utilisant des clés privées/publiques identiques (le `eepPriv.dat` traditionnel) peuvent héberger sur plusieurs routers simultanément. Chaque instance publie périodiquement des LeaseSets (descripteurs des tunnels d'entrée) signés ; le LeaseSet publié le plus récent est renvoyé aux clients effectuant une recherche. Avec une durée de vie maximale de 10 minutes pour les LeaseSets, les pannes durent au plus ~10 minutes.

À partir de la version 0.9.38, les **Meta LeaseSets** prennent en charge des services multi‑hébergés à grande échelle utilisant des Destinations (identité/adresse I2P) distinctes fournissant des services communs. Les entrées de Meta LeaseSet sont des Destinations ou d’autres Meta LeaseSets, avec des expirations pouvant aller jusqu’à 18,2 heures, ce qui permet à des centaines/des milliers de Destinations d’héberger des services communs.

---

## 10. Analyse des menaces

Environ 1700 floodfill routers (nœuds chargés de diffuser la netDb) opèrent actuellement. La croissance du réseau rend la plupart des attaques plus difficiles ou moins efficaces.

### 10.1 Mesures d’atténuation générales

- **Croissance**: Plus de floodfills rendent les attaques plus difficiles ou moins impactantes
- **Redondance**: Toutes les entrées netdb sont stockées sur 3 floodfill routers les plus proches de la clé via flooding (diffusion massive)
- **Signatures**: Toutes les entrées sont signées par leur créateur; les falsifications sont impossibles

### 10.2 Routers lents ou non réactifs

Routers maintiennent des statistiques étendues dans les profils de pairs pour les floodfills: - Temps de réponse moyen - Pourcentage de réponses aux requêtes - Pourcentage de réussite de la vérification du stockage - Dernier stockage réussi - Dernière recherche réussie - Dernière réponse

Les routers utilisent ces métrriques pour évaluer la "qualité" lors de la sélection du floodfill le plus proche. Les routers complètement non réactifs sont rapidement identifiés et évités; les routers partiellement malveillants posent un défi plus important.

### 10.3 Attaque Sybil (espace de clés complet)

Des attaquants pourraient créer de nombreux floodfill routers répartis dans l’ensemble du keyspace (espace de clés) afin de mener une attaque par déni de service (DoS) efficace.

Si le comportement n'est pas suffisamment problématique pour une désignation "bad", des réponses possibles comprennent : - Compilation de listes de hash/IP de router "bad" annoncées via les actualités de la console, le site web, le forum - Activation du floodfill à l'échelle du réseau ("combattre Sybil par plus de Sybil") - Nouvelles versions logicielles avec des listes "bad" codées en dur - Amélioration des métriques de profils de pairs et des seuils pour l'identification automatique - Qualification par bloc IP disqualifiant plusieurs floodfills au sein d'un même bloc IP - Liste noire automatique basée sur abonnement (similaire au consensus de Tor)

Les réseaux plus vastes rendent cela plus difficile.

### 10.4 Attaque Sybil (espace de clés partiel)

Des attaquants peuvent créer 8 à 15 routers floodfill étroitement regroupés dans l'espace de clés. Toutes les requêtes de recherche/stockage pour cet espace de clés aboutissent aux routers des attaquants, ce qui permet de lancer une attaque par déni de service (DoS) contre certains sites I2P.

Comme l'espace de clés indexe des hachages SHA256 cryptographiques, les attaquants doivent recourir à la force brute pour générer des routers suffisamment proches.

**Défense**: L’algorithme de proximité Kademlia (algorithme de table de hachage distribuée) varie au fil du temps en utilisant `SHA256(key + YYYYMMDD)`, changeant chaque jour à minuit UTC. Cette rotation de l’espace de clés impose une régénération quotidienne des attaques.

> **Note**: Des recherches récentes montrent que la rotation de l'espace de clés n'est pas particulièrement efficace — les attaquants peuvent précalculer les hachages de routers, ce qui ne requiert que quelques routers pour éclipser des portions de l'espace de clés dans la demi-heure suivant la rotation.

Conséquence de la rotation quotidienne: le netdb distribué devient peu fiable pendant plusieurs minutes après la rotation—les recherches échouent avant que le nouveau router le plus proche ne reçoive les messages de stockage.

### 10.5 Attaques d'amorçage

Des attaquants pourraient prendre le contrôle de reseed websites (sites servant à fournir les informations initiales du réseau I2P) ou tromper les développeurs pour ajouter des reseed websites hostiles, amenant de nouveaux routers à démarrer au sein de réseaux isolés ou majoritairement contrôlés.

**Défenses mises en œuvre:** - Récupérer des sous-ensembles de RouterInfo depuis plusieurs sites de reseed (réensemencement) plutôt que depuis un seul site - Surveillance du reseed hors du réseau, interrogeant périodiquement les sites - À partir de la 0.9.14, les paquets de données de reseed sont des fichiers zip signés avec vérification des signatures téléchargées (voir [spécification su3](/docs/specs/updates))

### 10.6 Capture des requêtes

Les routers floodfill pourraient "orienter" des pairs vers des routers contrôlés par un attaquant via les références renvoyées.

Peu probable via l'exploration en raison de sa faible fréquence ; les routers acquièrent des références de pairs principalement via la construction normale de tunnel.

À partir de la version 0.8.9, les recherches itératives sont implémentées. Les références floodfill dans `DatabaseSearchReplyMessage` sont suivies si elles sont plus proches de la clé de recherche. Les router qui effectuent la requête ne font pas confiance à la proximité déclarée des références. Les recherches se poursuivent même en l’absence de clés plus proches, jusqu’à expiration du délai ou atteinte du nombre maximal de requêtes, ce qui empêche le black-holing (mise en trou noir) malveillant.

### 10.7 Fuites d’informations

Les fuites d’informations de la DHT (table de hachage distribuée) dans I2P nécessitent des investigations supplémentaires. Les Floodfill routers observent les requêtes et recueillent des informations. Avec 20 % de nœuds malveillants, les menaces de type Sybil décrites précédemment deviennent problématiques pour plusieurs raisons.

---

## 11. Travaux futurs

- Chiffrement de bout en bout des recherches netDb supplémentaires et des réponses associées
- De meilleures méthodes de suivi des réponses aux recherches
- Méthodes d'atténuation des problèmes de fiabilité liés à la rotation de l'espace de clés

---

## 12. Références

